from discord.ui import Modal as _DModal, InputText, View as _DView, Item, Button
from discord import Interaction, Embed
from typing import TYPE_CHECKING
from functools import partial
from typing import TypeVar

if TYPE_CHECKING:
    from client import Client


class View(_DView):
    def __init__(
            self,
            *items: Item,
            timeout: float | None = None,
            disable_on_timeout: bool = False
    ) -> None:
        # ? black magic to stop the view from adding all items on creation and breaking when there's too many
        tmp, self.__view_children_items__ = self.__view_children_items__, []
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.__view_children_items__ = tmp

        for func in self.__view_children_items__:
            item: Item = func.__discord_ui_model_type__(
                **func.__discord_ui_model_kwargs__)
            item.callback = partial(func, self, item)
            item._view = self
            setattr(self, func.__name__, item)

    def add_items(self, *items: Item) -> None:
        for item in items:
            if item not in self.children:
                self.add_item(item)

    async def on_error(self, error: Exception, item: Item, interaction: Interaction) -> None:
        notes = getattr(error, '__notes__', [])

        if 'already_raised' in notes:
            return

        error.add_note('already_raised')
        embed = Embed(title='an error has occurred!', color=0xff6969)
        embed.add_field(name='error', value=str(error))

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if not 'suppress' in notes:
            raise error


class BackButton(Button):
    def __init__(self, views: list['SubView']) -> None:
        self.views = views

        super().__init__(
            label='<', style=2, row=2,
            custom_id='back_button'
        )

    async def callback(self, interaction: Interaction) -> None:
        self.views.pop()
        await self.views[-1].__on_back__()

        await interaction.response.edit_message(
            embed=self.views[-1].embed,
            view=self.views[-1]
        )


class SubView(View):
    def __init__(self, master: 'MasterView', **kwargs) -> None:
        super().__init__()
        self.master = master
        self.client = master.client
        self.embed = Embed(
            title='this should always be overridden in either __init__ or __ainit__',
            color=0xff6969
        )

    async def back_button(self) -> None:
        ...  # ? i want the linter to make it the right color

    async def interaction_check(self, interaction: Interaction) -> bool:
        if getattr(self, 'user', None) is None:
            return True

        return (
            interaction.user.id == self.user.id or
            interaction.user.id in self.client.owner_ids and
            self.client.project.config.dev_bypass
        )

    async def __ainit__(self) -> None:
        """async init, should always be called after initialization"""
        pass

    async def __on_back__(self) -> None:
        """called when this view is returned to from a back button press"""
        pass


SUBVIEW_TYPE = TypeVar('SUBVIEW_TYPE', bound=SubView)


class MasterView:
    def __init__(self, client: 'Client', embed_color: int) -> None:
        self.client = client
        self.embed_color = embed_color
        self.views = []

    def create_subview(self, view_cls: type[SUBVIEW_TYPE], *args, **kwargs) -> SUBVIEW_TYPE:
        """
        create a view class that inherits from SubView
        pass it into this function to create a back trail
        """
        view = view_cls(self, *args, **kwargs)

        if self.views:
            view.back_button = BackButton(self.views)

        self.views.append(view)
        return view


class CustomModal(_DModal):
    def __init__(self, title: str, children: list[InputText]) -> None:
        self.interaction = None
        super().__init__(*children, title=title)

    async def callback(self, interaction: Interaction):
        self.interaction = interaction
        self.stop()


class SubCog:
    def __init__(self) -> None:
        raise NotImplementedError('Do not instantiate a SubCog')
