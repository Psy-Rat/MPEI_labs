# Что

Небольшая ученическая программа, реализующая MLP нейронную сеть, распознающая [UCI ML hand-written digits datasets](https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits).

Поскольку проект давний, ученический, фактически являющийся лабораторной по выбору, то о никаком SOLID, KISS, DRY, YAGNI, а уж тем более MVC и прочей архитектуре речи не идёт.

# Запуск

В корне лежит файл mlp_2016.yml - это окружение anaconda.
Качаем [анаконду](https://docs.anaconda.com/anaconda/install/) полная ли версия, или миниконда — без разницы.

В папке, где лежит mlp_2016.yml:

> conda env create -f mlp_2016.yml

На префикс в файле внимания не обращаем: конда делает его сама, а потом ей же самой на него плевать.
После этого

> conda activate mlp_mnist_2016

Ну и запускам:

> python ./main/main.py

# Использование

<div style="text-align:right;"><blockquote>Не надо</blockquote> <i>~Парень, который не хотел умирац</i></div>  
  
</br>

Кнопка <b>training</b> обучит нейронку в двадцать эпох на датасете [load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html). На cpu за это время, понятное дело, можно успеть заварить чайку, поэтому, пока tkinter зависает, данные об оставшихся эпохах кидаются в консоль. Потом сверху рисуется график ошибки. Цветов много, потому что каждый цвет это отдельная цифра. Можно заметить, как иногда, при улучшении общих показателей, улетает градиент, скажем, цифры 6, она теперь становится везде 5-ой и т.д. В качестве оптимизации градиентного спуска используется [оптимизация Нестерова](https://vbystricky.github.io/2018/03/optimization_grad_desc.html#%D1%83%D1%81%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5-%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B-%D0%BD%D0%B5%D1%81%D1%82%D0%B5%D1%80%D0%BE%D0%B2%D0%B0-nesterov-accelerated-gradient), но это, очевидно, не современно: если бы гиперпараметры спуска [оптимизировались](https://vbystricky.github.io/2018/03/optimization_grad_desc.html#adam-adaptive-moment-estimation) по мере уменьшения ошибки, то, возможно, градиенты так бы не вылетали. Oh well. Тем не менее оно работает. Loss - [MSE](https://sebastianraschka.com/faq/docs/mse-derivative.html) (а не категориальная кросс этропия, как положено в таких случаях), активация - везде [сигмоида](https://beckernick.github.io/sigmoid-derivative-neural-network/), даже на выходе не софтмакс, ай-яй-яй, но на то проет и ученический, чтобы ломать ноги и учиться на ошибках, поэтому что есть. По хорошему разнести слои, функции ошибок, активации и оптимизацию градиентного спуска, но у меня не было задачи сделать свой собственный Tensorflow для CPU.
