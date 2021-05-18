# -------------------------------------------
# QtForms
from PyQt5 import QtCore, QtGui, QtWidgets
# -------------------------------------------
# FileWork
import wave
import os
import winsound
import struct
# -------------------------------------------
# Graphics
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# -------------------------------------------
from threading import Thread
# -------------------------------------------
# Math
# import scipy as sci
import numpy as np
import math
# -------------------------------------------
# Forms
import stegwindow
import windwaveinfo
# -------------------------------------------

# -------------------------------------------
# Settings
matplotlib.rcParams.update({'font.size': 8})
# -------------------------------------------
# constants
types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

codetype = {
    1: 8,
    2: 32
}

utf_length = 32
ascii_length = 8

key_length_min = 8
key_length_max = 255

str_default_container = "[ 0 \ 0]"
# ---------------------------------------------------------------------------------------------------------------------
# global
peak = 0
nframes = 0
k_str = 0
# ---------------------------------------------------------------------------------------------------------------------
# Head protocol: [len of type] 1b, [type] 1b x size, [len data] 4b, [type of code] 1b
# ---------------> 7b + len of type = 54 + [len of type  x  8]
headsize = 8+32
# ---------------------------------------------------------------------------------------------------------------------

# Получаем схему перестановочного ключа


def get_key(key):
    a = list(key)
    a.sort()
    result = []
    for char in a:
        padding = key.find(char)
        f_already_there = True
        while f_already_there:
            try:
                result.index(padding)
                padding += 1 + key[padding+1:].find(char)
            except Exception:
                f_already_there = False
        result.append(padding)
    return result
# ---------------------------------------------------------------------------------------------------------------------


def data_normalization(bincode, real_key):
    bincode = np.append(bincode, [1])
    while len(bincode) % len(real_key) > 0:
        bincode = np.append(bincode, [0])
    return bincode
# ---------------------------------------------------------------------------------------------------------------------


def encryption(bincode, key, progressbar=None):
    # or (len(bincode) < key_length_max)):
    if ((len(key) < key_length_min) or (len(key) > key_length_max)):
        print("Несоответствие параметрам")
        return -1

    real_key = get_key(key)

    bincode = data_normalization(bincode, real_key)

    for i in range(0, len(bincode), len(real_key)):
        new_buffer = []
        buffer = bincode[i:i + len(real_key)]
        if progressbar != None:
            progressbar.setValue(min(round(i/len(bincode)*100), 100))

        for ind in real_key:
            new_buffer.append(buffer[ind])

        for j in range(len(real_key)):
            bincode[i + j] = new_buffer[j]
    progressbar.setValue(100)
    return bincode
# ---------------------------------------------------------------------------------------------------------------------


def decryption(bincode, key, progressbar=None):
    real_key = get_key(key)
    length = len(bincode) - (len(bincode) % len(real_key))

    for i in range(0, length, len(real_key)):
        new_buffer = list(np.zeros(len(real_key)))
        buffer = bincode[i:i + len(real_key)]

        if progressbar != None:
            progressbar.setValue(min(round(i/len(bincode)*100), 100))

        for ind, buff in zip(real_key, buffer):
            new_buffer[ind] = buff

        for j in range(len(real_key)):
            bincode[i + j] = new_buffer[j]

    i_eof = len(bincode) - 1
    while not bincode[i_eof]:
        i_eof -= 1

    progressbar.setValue(100)

    bincode = bincode[0: i_eof]
    return bincode
# ---------------------------------------------------------------------------------------------------------------------

# y_formatter for wave info


def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"
    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)
# ---------------------------------------------------------------------------------------------------------------------

# x_formatter for wave info


def format_time(x, pos=None):
    global duration, nframes, k_str
    progress = int(x / float(nframes) * duration * k_str)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out
# ---------------------------------------------------------------------------------------------------------------------
# Из бинарного кода в представление utf


def get_utf32(string):
    m = np.zeros(utf_length)
    # Если это не utf, то маскируем ошибку точкой
    if len(list(string)[0:-1]) > utf_length:
        m[utf_length - len(np.binary_repr(ord('.')))
                           :] = list(np.binary_repr(ord('.')))[:]
    else:
        m[utf_length - len(string):] = list(string)[:]

    return list(map(int, m))

# ---------------------------------------------------------------------------------------------------------------------
# Из бинарного кода в представление ascii


def get_ascii(string):
    m = np.zeros(ascii_length)
    # Если это не ascii, то маскируем ошибку точкой
    if len(list(string)[0:-1]) > ascii_length:
        print(len(list(string)))
        print(string)
        m[ascii_length - len(np.binary_repr(ord('.')))
                             :] = list(np.binary_repr(ord('.')))[:]
    else:
        m[ascii_length - len(string):] = list(string)[:]
    return list(map(int, m))

# ---------------------------------------------------------------------------------------------------------------------
# Разбиение  списка на подсписки указанной длины


def split(aList, aLength):
    new_list = []
    for i in range(0, len(aList), aLength):
        new_list.append(aList[i: i + aLength])
    return list(new_list)

# ---------------------------------------------------------------------------------------------------------------------
# Перевод бинарного числа в десятичный вид


def bin2dec(aList):
    res = 0
    for i in range(len(aList)):
        res += aList[len(aList) - 1 - i] * 2 ** i
    return res

# ---------------------------------------------------------------------------------------------------------------------
# Перевод бинарного числа, записанного в список, в десятичное


def bin32todec(utf):
    result = 0
    for i in range(0, len(utf)):
        result += utf[i] * 2**(len(utf) - i - 1)
    return int(result)
# ---------------------------------------------------------------------------------------------------------------------
# Получения массива нулей и единиц, представляющих собой бинарное представление строки в заданном формате


def get_binary(aString, aFCoding):
    return (np.array(list(map(aFCoding, list(map(np.binary_repr, list(map(ord, list(aString))))))))).flatten()

# ---------------------------------------------------------------------------------------------------------------------
# Возвращение массива нулей и единиц, представляющих число в заданном коде


def dec2bin(aNumber, aFCoding):
    return (np.array(list(map(aFCoding, (list(map(np.binary_repr, [aNumber]))))))).flatten()

# ---------------------------------------------------------------------------------------------------------------------
# Вывод полученного файла


def outputting_wave(aFilename, paramtuple, aSamples, progressbar=None):
    file = wave.open(aFilename, 'wb')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = paramtuple
    file.setparams(paramtuple)
    for byte in range(2 * nframes):
        if progressbar != None:
            progressbar.setValue(min(round(byte / (2 * nframes) * 100), 100))
        buff = struct.pack('h', aSamples[byte])
        file.writeframes(buff)

    file.close()
# ---------------------------------------------------------------------------------------------------------------------

# Убираем наименее значащий бит


def odding(even):
    return even - even % 2

# ---------------------------------------------------------------------------------------------------------------------
# прячем сообщение в семплах


def hideMsg(message, inted_blob):
    if len(inted_blob) < len(message):
        print('Контейнер слишком мал')
        return None
    active_part = inted_blob[:len(message)]
    passive_part = inted_blob[len(message):]
    print(str(len(inted_blob)) + "=" +
          str(len(active_part)) + "+" + str(len(passive_part)))

    active_part = np.array(list(map(odding, active_part)))

    active_part += np.array(list(map(int, message)))

    inted_blob = np.append(active_part, passive_part, axis=0)

    return inted_blob

# ---------------------------------------------------------------------------------------------------------------------
# Получаем сообщение из блоба


def getMsg(blob):
    res = []
    for i in blob:
        res.append(i % 2)
    return res
# ---------------------------------------------------------------------------------------------------------------------
# Сбор строки из массива списков нулей и единиц


def reconstruct(aArray):
    strResult = ""
    for i in list(map(bin2dec, list(aArray))):
        strResult += chr(i)
    return strResult
# ---------------------------------------------------------------------------------------------------------------------


class PlayerThread(Thread):
    def __init__(self, button, wave):
        Thread.__init__(self)
        self.button = button
        self.wave = wave

    def run(self):
        try:
            self.button.setEnabled(False)
        except:
            return
        winsound.PlaySound(self.wave, winsound.SND_ALIAS)
        try:
            self.button.setEnabled(True)
        except:
            return
# ---------------------------------------------------------------------------------------------------------------------


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, data=None, width=4, height=2.5, dpi=100):

        print(data)
        print(data.nFrames)

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = None

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        if data is None:
            self.parent = None
            return
        self.data = data
        w, h = 800, 300

        self.DPI = 72
        global peak, k_str, duration, nframes
        peak = 256 ** data.Sampwidth / 2
        k_str = data.nFrames / w / 32
        duration = data.nFrames / data.Framerate
        nframes = data.nFrames

        self.plot()

    # Отрисовка
    def plot(self):
        global peak, k_str, duration, nframes
        print(k_str)
        for n in range(self.data.nChannels):
            channel = self.data.samples[n::self.data.nChannels]

            channel = channel[0::int(k_str)]
            if self.data.nChannels == 1:
                channel = channel - peak

            self.axes = self.fig.add_subplot(
                self.data.nChannels, 1, n + 1, facecolor="k")
            self.axes.plot(channel, "g")
            self.axes.yaxis.set_major_formatter(
                ticker.FuncFormatter(format_db))
            plt.grid(True, color="w")
            self.axes.xaxis.set_major_formatter(ticker.NullFormatter())

        self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
        self.draw()
# ---------------------------------------------------------------------------------------------------------------------


class Header():
    def __init__(self, type, length, content):
        self.type = type
        self.length = length
        self.content = content
# ---------------------------------------------------------------------------------------------------------------------


class Object():
    def __init__(self, type, content, form='txt'):
        self.Head = Header(8, len(form) * 8, form)
        # print(form)
        self.Core = Header(type, len(content) * type, content)

    def get_data(self):
        result = np.append(dec2bin(self.Head.type, get_ascii),
                           dec2bin(self.Head.length, get_utf32), axis=0)
        result = np.append(result,
                           get_binary(self.Head.content, get_ascii), axis=0)

        result = np.append(result,
                           dec2bin(self.Core.type, get_ascii), axis=0)
        result = np.append(result,
                           dec2bin(self.Core.length, get_utf32), axis=0)

        if self.Core.type is 8:
            result = np.append(result,
                               get_binary(self.Core.content, get_ascii), axis=0)
        else:
            result = np.append(result,
                               get_binary(self.Core.content, get_utf32), axis=0)

        return result

    @classmethod
    def from_inted_blob(cls, inted_blob):
        curr = 0
        numb_type = bin2dec(inted_blob[curr: curr + 8])
        curr += 8

        numb_length = bin2dec(inted_blob[curr: curr + 32])
        curr += 32
        str_form = ''

        if (numb_type == 8):
            str_form = reconstruct(
                list(split(inted_blob[curr: curr + numb_length], ascii_length)))
        if (numb_type == 32):
            str_form = reconstruct(
                list(split(inted_blob[curr: curr + numb_length], utf_length)))
        curr += numb_length

        numb_type = bin2dec(inted_blob[curr: curr + 8])
        curr += 8

        numb_length = bin2dec(inted_blob[curr: curr + 32])
        curr += 32
        str_content = ''

        if (numb_type == 8):
            str_content = reconstruct(
                list(split(inted_blob[curr: curr + numb_length], ascii_length)))
        if (numb_type == 32):
            str_content = reconstruct(
                list(split(inted_blob[curr: curr + numb_length], utf_length)))
        curr += numb_length

        return Object(numb_type, str_content, str_form)
# ---------------------------------------------------------------------------------------------------------------------


class Data():
    def __init__(self, nchannels, sampwidth, framerate, nframes, comptype, compname, frames):
        self.nChannels = nchannels
        self.Sampwidth = sampwidth
        self.Framerate = framerate
        self.nFrames = nframes
        self.nContainerMax = math.floor(
            self.nFrames / key_length_max - 1) * key_length_max
        self.comptype = comptype
        self.compname = compname
        self.type = types[sampwidth]
        self.samples = np.fromstring(frames, dtype=types[sampwidth])

    def get_tuple(self):
        return (self.nChannels, self.Sampwidth, self.Framerate, self.nFrames, self.comptype, self.compname)
# ---------------------------------------------------------------------------------------------------------------------

# Основной рабочий объект


class Worker():

    # Создание класса
    def __init__(self, aForm):
        self.currentClearWavPath = None
        self.currentDirtyWav = None
        self.Form = aForm
        self.Data = None
        self.SecondData = None
        self.showPass = False
        self.Message = None
        self.Head = None
        self.Code = utf_length
        self.CurrentSize = 0
        self.OpenObject = None
        self.encoded_blob = None
        self.Reconstr = None
        self.HiddenType = None
    # Смена кодировки сообщения

    def changeCode(self):
        type = 1
        if self.Form.rbASCII.isChecked():
            type = 1
        if self.Form.rbUTF.isChecked():
            type = 2
        self.Code = codetype[type]
        if self.Data == None:
            return
        self.printremains()
        self.onMessageChange()

    # Отрисовка оставшихся свободных бит стеганоконтейнера
    def printremains(self):
        headtext = self.Form.ledMesHead.text()
        self.Form.lblEnabledSize.setStyleSheet("QLabel { color: black }")
        curr_mes_weight = (self.Data.nFrames - self.Data.nContainerMax +
                           len(self.Form.teMessage.toPlainText()) * self.Code +
                           len(headtext) * 8)

        if curr_mes_weight > self.Data.nContainerMax:
            self.Form.lblEnabledSize.setStyleSheet("QLabel { color: red }")

        self.Form.lblEnabledSize.setText(
            "[" + str(curr_mes_weight) + '/' + str(self.Data.nFrames) + "]")

    # Загрузка "чистого" Wav файла
    def load_clearwav(self):
        self.Form.lblEnabledSize.setText(str_default_container)
        # Класс диалогового окна
        FileWid = QtWidgets.QFileDialog()
        # Берём путь к WAV файлу
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(FileWid, caption="Откройте аудиофайл для стеганографии",
                                                            filter="wave (*.wav)")
        if not os.path.isfile(fileName):
            return

        self.currentClearWavPath = os.path.realpath(fileName)
        # Выводим в поле edit
        self.Form.ledWavPath.setText(str(self.currentClearWavPath))
        # Собираем информацию из файла
        try:
            wav_sample = wave.open(self.currentClearWavPath, 'rb')
        except Exception as e:
            msg = QtWidgets.QMessageBox(None)
            msg.setText(str(e))
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return

        (nchannels, sampwidth, framerate, nframes,
         comptype, compname) = wav_sample.getparams()
        frames = wav_sample.readframes(nframes)
        self.Data = Data(nchannels, sampwidth, framerate,
                         nframes, comptype, compname, frames)
        self.Form.teMessage.setEnabled(True)
        wav_sample.close()

        # Выводим количество доступных бит для скрытия
        self.Form.teMessage.setPlainText('')
        self.CurrentSize = 0
        self.printremains()

    # Проиграть аудиофайл
    def playwav(self):
        winsound.PlaySound(self.currentClearWavPath, winsound.SND_ALIAS)

    # Отрисовать информацию о файле
    def printInfo(self, type=None):
        print('Main worker printInfo '+str(type))
        if type == 2:
            string = "Файл : " + str(self.currentClearWavPath) \
                + "\r\n***************************************" \
                + "\r\nКоличество каналов: " + str(self.Data.nChannels) \
                + "\r\nКоличество фреймов: " + str(self.Data.nFrames) \
                + "\r\nДлина одного сэмпла: " + str(self.Data.Sampwidth * 8) + "bit" \
                + "\r\nЧастота кадров :" + str(self.Data.Framerate) \
                + "\r\nСжатие: " + str(self.Data.compname)  \
                + "\r\n***************************************"
        else:
            string = "Файл : " + str(self.currentDirtyWav) \
                + "\r\n***************************************" \
                + "\r\nКоличество каналов: " + str(self.SecondData.nChannels) \
                + "\r\nКоличество фреймов: " + str(self.SecondData.nFrames) \
                + "\r\nДлина одного сэмпла: " + str(self.SecondData.Sampwidth * 8) + "bit" \
                + "\r\nЧастота кадров :" + str(self.SecondData.Framerate) \
                + "\r\nСжатие: " + str(self.SecondData.compname)  \
                + "\r\n***************************************"

        msg = QtWidgets.QMessageBox(None)
        msg.setText(string)
        msg.setWindowTitle("Информация")
        msg.exec()

    # Реакция на изменение текста сообщения
    def onMessageChange(self):
        if not self.currentClearWavPath is None:
            self.HiddenType = "txt"
            self.Head = "3;txt;" + \
                str(self.Code) + ";" + \
                str(len(self.Form.teMessage.toPlainText()) * self.Code)
            self.Form.ledMesHead.setText(self.Head)
            self.printremains()

    # Скрыть/показать пароль

    def changeEcho(self):
        if self.showPass:
            self.showPass = False
            self.Form.ledPassword.setEchoMode(QtWidgets.QLineEdit.Password)
            self.Form.ledPasswordRepeat.setEchoMode(
                QtWidgets.QLineEdit.Password)
        else:
            self.showPass = True
            self.Form.ledPassword.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.Form.ledPasswordRepeat.setEchoMode(QtWidgets.QLineEdit.Normal)

    # Загрузить бинарный файл для вложения
    def binaryLoad(self):
        # Класс диалогового окна
        FileWid = QtWidgets.QFileDialog()
        # Загружаем файл
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(FileWid, caption="Откройте аудиофайл для вложения",
                                                            filter="Any(*.*)")
        if not os.path.isfile(fileName):
            return

        a = None
        try:
            with open(fileName, 'rb') as f:
                a = f.read()
        except Exception:
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Возникли ошибки при чтении файла")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return
        str_a = ''
        for i in a:
            str_a += chr(i)

        self.Form.rbASCII.setChecked(True)
        self.Form.rbUTF.setChecked(False)

        typename = fileName[fileName.rfind('.')+1:]
        print(typename)
        self.Code = codetype[1]
        self.Form.teMessage.setPlainText(str_a)

        self.HiddenType = typename

        self.Head = "3;"+typename+";" + \
            str(self.Code) + ";" + str(len(self.Form.teMessage.toPlainText()) * 8)
        self.Form.ledMesHead.setText(self.Head)
        self.printremains()

    def merger(self):
        if (len(self.Form.ledPassword.text()) < key_length_min) or (key_length_max < len(self.Form.ledPassword.text())):
            msg = QtWidgets.QMessageBox(None)
            msg.setText(
                "Пароль должен быть не короче 8 символов и не длиннее 256")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return
        if (self.Form.ledPassword.text() != self.Form.ledPasswordRepeat.text()):
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Пароли не совпадают")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return
        if (len(self.Form.teMessage.toPlainText()) <= 0):
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Сообщение для сокрытия отсутствует")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return

        # Случай текстового сообщения
        unenc = Object(
            self.Code, self.Form.teMessage.toPlainText(), self.HiddenType)
        unenc_data = unenc.get_data()
        self.Form.lblCurrStat.setText("Шифрование сообщения")
        enc_bin = encryption(
            unenc_data, self.Form.ledPassword.text(), self.Form.loadbar)
        self.Form.loadbar.setValue(0)
        self.Form.lblCurrStat.setText("...")

        FileWid = QtWidgets.QFileDialog()
        Filename, _ = QtWidgets.QFileDialog.getSaveFileName(FileWid, caption="Сохраните файл с сообщением",
                                                            filter="wave (*.wav)")

        new_samples = hideMsg(enc_bin, self.Data.samples)
        self.Form.lblCurrStat.setText("Запись в файл")
        outputting_wave(Filename, self.Data.get_tuple(),
                        new_samples,  self.Form.loadbar)
        self.Form.loadbar.setValue(0)
        self.Form.lblCurrStat.setText("...")


# ---------------------------------------------------------------------------------------------------------------------


    def open_steg(self):
        # Класс диалогового окна
        FileWid = QtWidgets.QFileDialog()
        # Берём путь к WAV файлу
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(FileWid, caption="Откройте аудиофайл для стеганографии",
                                                            filter="wave (*.wav)")
        if not os.path.isfile(fileName):
            return

        dirty_wav = os.path.realpath(fileName)
        self.currentDirtyWav = dirty_wav
        # Выводим в поле edit
        self.Form.ledOpenSteg.setText(str(dirty_wav))
        # Собираем информацию из файла
        try:
            wav_sample = wave.open(dirty_wav)
        except Exception:
            msg = QtWidgets.QMessageBox(None)
            msg.setText(Exception.__repr__())
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return

        (nchannels, sampwidth, framerate, nframes,
         comptype, compname) = wav_sample.getparams()
        frames = wav_sample.readframes(nframes)
        self.SecondData = Data(nchannels, sampwidth,
                               framerate, nframes, comptype, compname, frames)

        wav_sample.close()
        curr_samples = np.fromstring(frames, dtype=types[sampwidth])
        self.encoded_blob = getMsg(curr_samples)

    def get_out_steg(self):
        if (len(self.Form.ledPasswordDec.text()) < key_length_min) or (key_length_max < len(self.Form.ledPasswordDec.text())):
            msg = QtWidgets.QMessageBox(None)
            msg.setText(
                "Пароль должен быть не короче 8 символов и не длиннее 256")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            return

        ferror = 0

        buffer_enc = list(self.encoded_blob)
        self.Form.lblCurrStat.setText("Декодирование")
        try:
            dec_bin = decryption(
                buffer_enc, self.Form.ledPasswordDec.text(), self.Form.loadbar)
        except Exception:
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Ошибка при расшифровке. Неверный пароль?")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            ferror = 1

        self.Form.loadbar.setValue(0)
        self.Form.lblCurrStat.setText("...")

        if ferror == 1:
            return

        self.Form.lblCurrStat.setText("Восстановление")
        try:
            self.Form.loadbar.setValue(30)
            reconstr = Object.from_inted_blob(dec_bin)
            self.Form.loadbar.setValue(90)
        except Exception:
            msg = QtWidgets.QMessageBox(None)
            msg.setText(
                "Ошибка при распаковке. Неверный заголовок или отсутствие сообщения.")
            msg.setWindowTitle("Ошибка!")
            msg.exec()
            ferror = 1

        self.Form.loadbar.setValue(0)
        self.Form.lblCurrStat.setText("...")

        if ferror == 1:
            return

        if reconstr.Core.length == 0:
            msg = QtWidgets.QMessageBox(None)
            msg.setText("Полученное сообщение пусто. Неверный пароль?")
            msg.setWindowTitle("Ошибка!")
            msg.exec()

        self.Form.ted_extracted.setPlainText('********************\r\ntype = ' +
                                             reconstr.Head.content +
                                             "\r\n********************\r\n" +
                                             reconstr.Core.content)
        print(reconstr.Core.content)

        self.Reconstr = reconstr

    def save_decription(self):
        if self.Reconstr == None:
            return

        FileWid = QtWidgets.QFileDialog()
        filter_text = "output (*." + self.Reconstr.Head.content + ")"
        Filename, _ = QtWidgets.QFileDialog.getSaveFileName(FileWid, caption="Сохранение сообщения",
                                                            filter=filter_text)
        self.Form.lblCurrStat.setText("Запись в файл")

        if self.Reconstr.Head.content == 'txt':
            with open(Filename, 'w') as f:
                f.write(self.Reconstr.Core.content)
                return

        stringer = self.Reconstr.Core.content
        byter = list(map(ord, list(stringer)))
        newByteArray = bytearray(byter)
        try:
            with open(Filename, 'wb') as f:
                f.write(newByteArray)
        except Exception:
            return

        self.Form.loadbar.setValue(0)
        self.Form.lblCurrStat.setText("...")
