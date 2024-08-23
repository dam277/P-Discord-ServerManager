import nextcord

from ....database.models.tables.Note import Note

class PageView(nextcord.ui.View):
    """ # PageView class

    Description :
    ---
        Manage the discord page view

    Access :
    ---
        src.bots._views.PageView.py\n
        PageView

    inheritance :
    ---
        - View : :class:`View` => Parent class of page views
    """
    def __init__(self, pages: list[list[Note]], current_page: int = 0):
        """ # PageView constructor

        Description :
        ---
            Construct a PageView object

        Access :
        ---
            src.bots._views.PageView.py\n
            PageView.__init__()

        Parameters :
        ---
            - pages : :class:`list` => List of pages
            - current_page : :class:`int` => Index of the current page

        Returns :
        ---
            :class:`None`
        """
        super().__init__()

        self.pages = pages
        self.current_page = current_page


    @nextcord.ui.button(label='Previous', style=nextcord.ButtonStyle.blurple)
    async def previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Previous button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Go to the previous page

        Access :
        ---
            src.bots._views.PageView.py\n
            PageView.previous()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button that was pressed
            - interaction : :class:`nextcord.Interaction` => Interaction with the user

        Returns :
        ---
            :class:`None`
        """
        if self.current_page > 0:
            self.current_page -= 1
            await self.build_page(interaction)
            

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.blurple)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ Next button
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Go to the next page

        Access :
        ---
            src.bots._views.PageView.py\n
            PageView.next()

        Parameters :
        ---
            - button : :class:`nextcord.ui.Button` => Button that was pressed
            - interaction : :class:`nextcord.Interaction` => Interaction with the user

        Returns :
        ---
            :class:`None`
        """
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.build_page(interaction)
            
    async def build_page(self, interaction: nextcord.Interaction):
        """ # Build page function
        /!\\ This is a coroutine, it needs to be awaited

        Description :
        ---
            Build the page

        Access :
        ---
            src.bots._views.PageView.py\n
            PageView.build_page()

        Parameters :
        ---
            :class:`None`

        Returns :
        ---
            :class:`None`
        """
        # Create the embed
        page = self.pages[self.current_page]

        embed = nextcord.Embed(title=interaction.message.embeds[0].title)
        embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")

        # Add the notes to the embed
        for note in page:
            embed.add_field(name=note.title, value=note.text, inline=False)

        # Edit the message with the new embed
        await interaction.response.edit_message(embed=embed)