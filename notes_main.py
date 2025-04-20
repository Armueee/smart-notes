#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QLabel, QMessageBox, QRadioButton, QGroupBox, QVBoxLayout, QButtonGroup, QListWidget, QTextEdit, QLineEdit, QInputDialog
import json


def in_file(data):
    with open ('notes_data.json','w', encoding ='utf-8') as file:
        json.dump(data, file)

def out_file():
    with open ('notes_data.json','r', encoding ='utf-8') as file:
        data = json.load(file)
        return data

def show_note():
    name = list_notes.selectedItems()[0].text()
    main_notes.setText(notes[name]['текст'])
    teg_list.clear()
    teg_list.addItems(notes[name]['теги'])
    in_file(notes)

def add_note():
    note_name, result = QInputDialog.getText(main_win,'Добавить заметку', 'Название заметки:')
    notes[note_name] ={'текст':'','теги':[]}
    list_notes.addItem(note_name)
    teg_list.addItems(notes[note_name]['теги'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        teg_list.clear()
        main_notes.clear()
        in_file(notes)
        list_notes.addItems(list(notes.keys()))

def save_note():
    if list_notes.selectedItems():
        note_text = main_notes.toPlainText()
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = note_text
        in_file(notes)

def search_tagf():
    tag = add_to_teg.text()
    if found_teg.text() == 'Искать заметки по тегу' and tag:
        lst = []
        for note in notes:
            if tag in notes[note]['теги']:
                lst.append(note)
        found_teg.setText('Сбросить поиск')
        list_notes.clear()
        teg_list.clear()
        add_to_teg.clear()
        list_notes.addItems(lst) 
    elif found_teg.text() == 'Сбросить поиск':
        list_notes.clear()
        teg_list.clear()
        add_to_teg.clear()
        list_notes.addItems(notes.keys())
        found_teg.setText('Искать заметки по тегу')
    else:
        pass

def add_tegf():
    if list_notes.selectedItems():
        tag = add_to_teg.text()
        add_to_teg.clear()
        if tag:
            name = list_notes.selectedItems()[0].text()
            notes[name]['теги'].append(tag)
            teg_list.addItem(tag)
            in_file(notes)

def del_tegf():
    if list_notes.selectedItems() and teg_list.selectedItems():
        note = list_notes.selectedItems()[0].text()
        tag = teg_list.selectedItems()[0].text()
        for i in range(len(notes[note]['теги'])):
            if notes[note]['теги'][i] == tag:
                del notes[note]['теги'][i]
        teg_list.clear()
        teg_list.addItems(notes[note]['теги'])

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_notes = QTextEdit()#ввод заметки
list_notes = QListWidget()#список заметок
teg_list = QListWidget()#список тегов 
addnotes = QPushButton('Создать заметку')#Создать заметку(NOTES)
delete_notes = QPushButton('Удалить заметку')#Удалить заметку(NOTES)
save_notes = QPushButton('Сохранить заметку')#Сохранить заметку(NOTES)
add_teg = QPushButton('Добавить к заметке')#Добавить к заметке(TEGS)
unpin_teg = QPushButton('Открепить от заметки')#Открепить от заметки(TEGS)
found_teg = QPushButton('Искать заметки по тегу')#Искать заметки по тегу(notes(teg))\
add_to_teg = QLineEdit()

main_win.resize(800, 650)

Horiz1 = QHBoxLayout()
Horiz2 = QHBoxLayout()

Horiz1.addWidget(addnotes)
Horiz1.addWidget(delete_notes)
Horiz2.addWidget(add_teg)
Horiz2.addWidget(unpin_teg)


main_layout = QHBoxLayout()
left = QVBoxLayout()
right = QVBoxLayout()


left.addWidget(main_notes)
right.addWidget(list_notes)
right.addLayout(Horiz1)
right.addWidget(save_notes)
right.addWidget(teg_list)
right.addWidget(add_to_teg)
right.addLayout(Horiz2)
right.addWidget(found_teg)
main_layout.addLayout(right)
main_layout.addLayout(left)
main_win.setLayout(main_layout)

notes = out_file()
list_notes.itemClicked.connect(show_note)
list_notes.addItems(list(notes.keys()))

addnotes.clicked.connect(add_note)
delete_notes.clicked.connect(del_note)
add_teg.clicked.connect(add_tegf)
save_notes.clicked.connect(save_note)
unpin_teg.clicked.connect(del_tegf)
found_teg.clicked.connect(search_tagf)

# main_win.setStyleSheet("background-color: yellow;")
# list_notes.setStyleSheet("color: white ;")
main_win.show()
app.exec_()
