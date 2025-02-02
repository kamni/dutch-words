"""
Copyright (C) J Leadbetter <j@jleadbetter.com>
Affero GPL v3
"""

from nicegui import ui
'''
from nicegui.events import ValueChangeEventArguments

ui.label('Hello there!')
ui.icon('thumb_up')
ui.markdown('This is **Markdown**.')
ui.html('This is <strong>HTML</strong>.')
with ui.row():
    ui.label('CSS').style('color: #888; font-weight: bold')
    ui.label('Tailwind').classes('font-serif')
    ui.label('Quasar').classes('q-ml-xl')
ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

ui.button('Button', on_click=lambda: ui.notify('Click'))
with ui.row():
    ui.checkbox('Checkbox', on_change=show)
    ui.switch('Switch', on_change=show)
ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
with ui.row():
    ui.input('Text input', on_change=show)
    ui.select(['One', 'Two'], value='One', on_change=show)
ui.link('And many more...', '/documentation').classes('mt-8')

class Demo:
    def __init__(self):
        self.number = 1

demo = Demo()
v = ui.checkbox('visible', value=True)
with ui.column().bind_visibility_from(v, 'value'):
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
    ui.number().bind_value(demo, 'number')

documents = [('Dutch', ['Roodkapje']), ('English', ['Little Red Riding Hood'])]

with ui.column():
    for section, doc_list in documents:
        with ui.expansion(section, icon='work').classes('w-full'):
            with ui.column():
                for doc in doc_list:
                    ui.label(doc)

'''

document = {
    'sentences': ['Foo bar.', 'Baz' ],
}

documents = [('Dutch', ['Roodkapje']), ('English', ['Little Red Riding Hood'])]

def DocumentList(documents):
    with ui.column().classes():
        for section, doc_list in documents:
            with ui.expansion(section, icon='folder'):
                with ui.column():
                    for doc in doc_list:
                        ui.label(doc)

def DocumentDisplay(document):
    for sentence in document['sentences']:
        with ui.card():
            ui.label(sentence)


def Header():
    with ui.header():
        ui.label('10,000 Words')


Header()
with ui.row():
    DocumentList(documents)
    DocumentDisplay(document)


ui.run()
