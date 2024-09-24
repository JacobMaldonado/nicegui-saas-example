from nicegui import app, ui, APIRouter, events, run
from starlette.formparsers import MultiPartParser
from fastapi import Depends

from domain.UserManagementUseCase import UserManagementUseCase
from pages.components.header import header
import pages.components.user as user
from domain.GetVideoInsightsUseCase import GetVideoInsightsUseCase
from models.UploadFile import UploadFile
from constants import USER_INFO

MultiPartParser.max_file_size = 1024 * 1024 * 5  # 5 MB

router = APIRouter(prefix='/video')


@router.page('/')
async def example_page(
        use_case: GetVideoInsightsUseCase = Depends(GetVideoInsightsUseCase),
        use_case_user_management: UserManagementUseCase = Depends(UserManagementUseCase)):
    user.add_head_descope_scripts()
    header()
    async def get_bytes(event: events.UploadEventArguments):
        ui.notify(f'Processing {event.name}')
        print(app.storage.user.get(USER_INFO, {}).get('credits'))
        try:
            user = await run.io_bound(use_case_user_management.consume_credit, app.storage.user.get(USER_INFO, {}).get('id'), 1)
        except Exception as e:
            ui.notify(f'Error: {e}', position='center', color='red')
            return
        app.storage.user[USER_INFO]['credits'] = user.credits
        upload_file = UploadFile(file=event.content.read(), file_name=event.name, type=event.type)
        try:
            result = await run.io_bound(use_case.execute, upload_file, app.storage.user[USER_INFO]['plan'])
        except Exception as e:
            ui.notify(f'Error: {e}', position='center', color='red')
            return
        ui.notify(f'Completed {event.name} with Id {result}')
        ui.navigate.to(f'/video/analysis/{result}')

    with ui.element('div').classes('w-full'):
        with ui.element('div').classes('bg-gray-900 max-w-4xl mx-auto rounded-lg shadow-lg p-4'):
            if app.storage.user.get(USER_INFO, {}).get('plan') != 'paid':
                with ui.element('div').classes('w-full flex justify-end'):
                    ui.button('Upgrade').on_click(lambda: ui.navigate.to('/upgrade')).classes('mt-4 mb-4 ').props('color="purple"')
            ui.label('Record Yourself').classes('text-3xl mb-4 font-bold text-gray-200 text-center block ')
            ui.label('Record an audio or video in advance of your pitch, presentation or talk').classes('text-gray-200 mb-10 text-center text-xl')
            ui.label('Upload a file').classes('text-3xl mb-20 font-bold text-gray-200 text-center block ')
            ui.label('Drag and drop a file here or click the + icon').classes('text-gray-200 mb-4 text-center md:hidden')
            with ui.element('div').classes('mx-auto mb-40 md:w-full md:flex md:justify-center md:flex-nowrap'):
                ui.upload(on_upload=get_bytes, auto_upload=True).props('accept="video/*,audio/*"').classes('rounded-lg max-md:mx-auto')
                with ui.element('div').classes('flex w-1/4 max-md:hidden flex-none flex-nowrap'):
                    ui.icon('arrow_back').classes('ml-4 text-gray-200 text-4xl w-1/12')
                    ui.label('Click here to upload a video or audio').classes('flex-1 text-gray-200 text-xl ml-4 text-balance')
            
    await ui.context.client.connected()
    await user.validate_user_session('/video')