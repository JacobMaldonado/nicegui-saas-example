from nicegui import ui, APIRouter, run
from domain.AnalyzeVideoUseCase import AnalyzeVideoUseCase
from pages.components.header import header
from pages.components.inner_loading import inner_loading
import pages.components.user as user

router = APIRouter(prefix='/video')

@router.page('/analysis/{id}')
async def video_analysis_page(id: str):
    user.add_head_descope_scripts()
    header()
    async def load_remote_analysis():
        result = AnalyzeVideoUseCase().get_analysis(id)
        print(result)
        if result is None:
            return

        if result.title is not None:
            title_label.text = f'Project: {result.title}'
            loading_title.props(remove='showing')
        if result.file_url is not None:
            audio.source = result.file_url
        if result.overview is None:
            await get_analysis()
        else:
            sumary_text.content = result.overview.content
            key_ideas_text.content = result.overview.key_ideas
            questions_text.content = result.prepare.content
            audience_text.content = result.prepare.audience_questions
            mistakes_text.content = result.improve.mistakes
            suggestions_text.content = result.improve.recomendations
            loading_improvements.props(remove='showing')
            loading_questions.props(remove='showing')
            loading_overview.props(remove='showing')


    async def get_analysis():
        loading_overview.props('showing')
        loading_questions.props('showing')
        loading_improvements.props('showing')
        ui.notify('Started Overview Analysis')
        await sumarize_text()
        loading_overview.props(remove='showing')
        ui.notify('Started Prepare Analysis')
        await get_questions()
        loading_questions.props(remove='showing')
        ui.notify('Started Improve Analysis')
        await improve_transcript()
        loading_improvements.props(remove='showing')
        ui.notify('Analysis Completed')

    async def sumarize_text():
        result = await run.io_bound(AnalyzeVideoUseCase().analyze_main_idea, f'./audios/{id}.mp3', id)
        sumary_text.content = result['overview']
        key_ideas_text.content = result['key_ideas']

    async def get_questions():
        result = await run.io_bound(AnalyzeVideoUseCase().analyze_questions, f'./audios/{id}.mp3', id)
        questions_text.content = result['questions']
        audience_text.content = result['audience_questions']

    async def improve_transcript():
        result = await run.io_bound(AnalyzeVideoUseCase().improve_transcript, f'./audios/{id}.mp3', id)
        mistakes_text.content = result['mistakes']
        suggestions_text.content = result['recomendations']

    with ui.element('div').classes('w-full bg-gray-200 min-h-screen'):
        with ui.element('div').classes('bg-gray-900 max-w-4xl mx-auto rounded-lg shadow-lg p-4'):
            with ui.element('div').classes('flex w-full justify-end'):
                ui.button('New').on_click(lambda: ui.navigate.to('/video')).classes('text-gray-200 text-center m-4')
            title_label = ui.label(f'Analysis for video {id}').classes('text-3xl mb-20 font-bold text-gray-200 text-center block ')
            audio = ui.audio(f'https://storage.googleapis.com/audio-files-confidentier/{id}.mp3', autoplay=False).classes('rounded-lg mx-auto')
            loading_title = inner_loading()
        with ui.element('div').classes('mt-8 bg-gray-900 max-w-4xl mx-auto rounded-lg shadow-lg p-4 text-gray-200'):
            ui.label('Analysis').classes('text-4xl font-bold text-gray-200 text-center block mb-4')
            with ui.tabs().classes('w-full') as tabs:
                overview = ui.tab('Overview')
                questions = ui.tab('Prepare')
                improvements = ui.tab('Improve')
            with ui.tab_panels(tabs, value=overview).classes('w-full bg-gray-900'):
                with ui.tab_panel(overview):
                    ui.label('Summary').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    sumary_text = ui.markdown('')
                    ui.label('Key ideas').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    key_ideas_text = ui.markdown('')
                    loading_overview = inner_loading()
                with ui.tab_panel(questions):
                    ui.label('Audience').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    audience_text = ui.markdown('')
                    ui.label('Questions that audience may have').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    questions_text = ui.markdown('')
                    loading_questions = inner_loading()
                with ui.tab_panel(improvements):
                    ui.label('Mistakes').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    mistakes_text = ui.markdown('')
                    ui.label('Suggestions').classes('text-2xl font-bold text-gray-200 text-center block mb-4')
                    suggestions_text = ui.markdown('')
                    loading_improvements = inner_loading()
    await ui.context.client.connected()
    await user.validate_user_session(f'/video/analysis/{id}')
    await load_remote_analysis()
