import tensorflow as tf

from models.one_step import OneStep
from models.modelo import Modelo


def config():
    # CONFIGURAÇÃO
    path = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

    text = open(path, 'rb').read().decode(encoding='utf8')

    print(f'Tamanho do texto: {len(text)} caracteres')

    print(text[:250])

    vocabulario = sorted(set(text))


    ids_chars = tf.keras.layers.StringLookup(vocabulary=list(vocabulario), mask_token=None)

    all_ids = ids_chars(tf.strings.unicode_split(text, 'UTF-8'))
    ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

    embedding_dimension = 256

    # número de unidades de redes neurais
    rnn_units = 1024

    chars_ids = tf.keras.layers.StringLookup(vocabulary=ids_chars.get_vocabulary(), invert=True, mask_token=None)

    return text, vocabulario, ids_chars, chars_ids, ids_dataset, embedding_dimension, rnn_units

def executa_treinamento():
    epochs = 20

    history = model.fit()

def constroi_modelo():
    modelo =  Modelo(
        vocab_size=len(ids_chars.get_vocabulary()),
        embedding_dim=embedding_dimension,
        rnn_units=rnn_units
    )

    return modelo

def salva_modelo():
    tf.saved_model.save(model, 'one_step')

def divide_input_alvo(seq):
    input_text = seq[:-1]
    target_text = seq[1:]
    return input_text, target_text

seq_length = 100

text, vocabulario, ids_chars, chars_ids, ids_dataset, embedding_dimension, rnn_units = config()


sequencias = ids_dataset.batch(seq_length+1, drop_remainder=True)

dataset = sequencias.map(divide_input_alvo)

BATCH_SIZE = 64

BUFFER_SIZE = 10000

dataset = (
    dataset
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)



model = constroi_modelo()

perda = tf.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam', loss=perda)

one_step_model = OneStep(model, chars_ids, ids_chars)

