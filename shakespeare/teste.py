import tensorflow as tf
import numpy as np
import os
import time

def text_from_ids(ids):
    return tf.strings.reduce_join(chars_ids(ids), axis=-1)

def train():
    EPOCHS = 20

    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])

def salvar_modelo(modelo, nome_modelo):
    tf.saved_model.save(modelo, nome_modelo)

def carregar_modelo(nome_modelo):
    return tf.saved_model

path = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

text = open(path, 'rb').read().decode(encoding='utf8')

print(f'Tamanho do texto: {len(text)} caracteres')

print(text[:250])

vocabulario = sorted(set(text))

print(f'{len(vocabulario)} caracteres únicos')

texts_exemplo = ['abcdefg', 'xyz']

caracteres = tf.strings.unicode_split(texts_exemplo, input_encoding='UTF-8')

ids_chars = tf.keras.layers.StringLookup(vocabulary=list(vocabulario), mask_token=None)

ids = ids_chars(caracteres)

chars_ids = tf.keras.layers.StringLookup(vocabulary=ids_chars.get_vocabulary(), invert=True, mask_token=None)

chars = chars_ids(ids)

tf.strings.reduce_join(chars, axis=-1).numpy()

all_ids = ids_chars(tf.strings.unicode_split(text, 'UTF-8'))

ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

for ids in ids_dataset.take(10):
    print(chars_ids(ids).numpy().decode('utf-8'))

seq_length = 100

exemplos_por_epoch = len(text)

sequencias = ids_dataset.batch(seq_length+1, drop_remainder=True)

for seq in sequencias.take(5):
    print(text_from_ids(seq).numpy())


def divide_input_alvo(sequencia):
    input_text = sequencia[:-1]
    target_text = sequencia[1:]
    return input_text, target_text

divide_input_alvo(list("TensorFlow"))

dataset = sequencias.map(divide_input_alvo)

for input_exemplo, target_exemplo in dataset.take(1):
    print("Input: ", text_from_ids(input_exemplo).numpy())
    print("Target: ", text_from_ids(target_exemplo).numpy())

BATCH_SIZE = 64

BUFFER_SIZE = 10000

dataset = (
    dataset
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)

# construir modelo
# tamanho do vocabulário em caracteres
vocab_size = len(vocabulario)

# embedding dimension
embedding_dimension = 256

# número de unidades de redes neurais
rnn_units = 1024

class Modelo(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(rnn_units,
                                       return_sequences=True,
                                       return_state=True)

        self.dense = tf.keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)

        if states is None:
            states = self.gru.get_initial_state(x)

        x, states = self.gru(x, initial_state=states, training=training)
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x

model = Modelo(
    vocab_size=len(ids_chars.get_vocabulary()),
    embedding_dim=embedding_dimension,
    rnn_units=rnn_units
)

for input_exemplo_batch, target_exemplo_batch in dataset.take(1):
    exemplo_batch_previsoes = model(input_exemplo_batch)
    print(exemplo_batch_previsoes.shape, "# (batch_size, sequence_length, vocab_size)")

model.summary()

exp_indices = tf.random.categorical(exemplo_batch_previsoes[0], num_samples=1)
exp_indices = tf.squeeze(exp_indices, axis=-1).numpy()


print("Input:\n", text_from_ids(input_exemplo_batch[0]).numpy())
print()
print("Próximos prováveis caracter:\n", text_from_ids(exp_indices).numpy())


## Treino do modelo

# utilizando a função de perda padrão do tensorflow

perda = tf.losses.SparseCategoricalCrossentropy(from_logits=True)

exemplo_batch_media_de_perdas = perda(target_exemplo_batch, exemplo_batch_previsoes)
print("Shape da previsão: ", exemplo_batch_previsoes, " # (batch_size, sequence_length, vocab_size)")
print("Média de perda: ", exemplo_batch_media_de_perdas)

model.compile(optimizer='adam', loss=perda)

## configurar pontos de verificação
# diretório onde os checkpoints serão salvos

checkpoint_dir = './training_checkpoints'

# nome dos arquivos de checkpoints
checkpoint_prefixo = os.path.join(checkpoint_dir, 'ckpt_{epoch}')

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefixo,
    save_weights_only=True
)

## EXECUTAR O TREINAMENTO
# para manter o tempo de treinamento razoável, usar 10 épocas para treinar o modelo.
# Agora, tenho que definir o tempo de execução para GPU para um treinamento mais rápido

train()

## GERAR O TEXTO
# a forma mais simples de gerar texto com esse modelo é executá-lo em um loop e acompanhar
# o estado interno do modelo à medida que o executamos

# cada vez que chamamos o modelo passamos algum texto e um estado interno. O modelo
# retorna uma previsão para o próximo caracter e seu novo estado. Vou passar a previsão
# e o estado de volta para continuar gerando texto

# o código abaixo faz uma previsão de uma única etapa

class OneStep(tf.keras.Model):
    def __init__(self, model, chars_ids, ids_chars, temperature=1.0):
        super().__init__()
        self.temperature = temperature
        self.model = model
        self.chars_ids = chars_ids
        self.ids_chars = ids_chars

        # crio uma máscara para prevenir que "[UNK]" seja gerado
        skip_ids = self.ids_chars(['[UNK]'])[:, None]
        sparse_mask = tf.SparseTensor(
            # colocar um -inf em cada bad indice
            values=[-float('inf')] * len(skip_ids),
            indices=skip_ids,
            # combinar o shape para o vocabulário
            dense_shape=[len(ids_chars.get_vocabulary())]
        )
        self.previsao_mask = tf.sparse.to_dense(sparse_mask)

    @tf.function
    def generate_one_step(self, inputs, states=None):
        # converte strings em token IDS
        input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
        input_ids = self.ids_chars(input_chars).to_tensor()

        # executa o model
        # previsao_logits.shape = [batch, char, next_char_logits]
        previsao_logits, states = self.model(inputs=input_ids, states=states, return_state=True)

        # somente usa a última previsão
        previsao_logits = previsao_logits[:, -1, :]
        previsao_logits = previsao_logits / self.temperature

        # aplica a máscara de previsão: evita [UNK] de ser gerado
        previsao_logits = previsao_logits + self.previsao_mask

        previsao_ids = tf.random.categorical(previsao_logits, num_samples=1)
        previsao_ids = tf.squeeze(previsao_ids, axis=-1)

        # converte os token ids em caracteres
        previsao_chars = self.chars_ids(previsao_ids)

        # retorna os caracteres e o estado do model
        return previsao_chars, states

one_step_model = OneStep(model, chars_ids, ids_chars)

# vamos executá-lo em loop para gerar algum texto. Observando o texto gerado, podemos
# ver que o modelo sabe quando capitalizar, fazer parágrafos e imita um vocabulário
# de escrita semelhante a Shakespeare. Com o pequeno número de épocas de treinamento,
# ainda não aprendeu a formar frases coerentes

start = time.time()
states = None
proximo_char = tf.constant(['ROMEO:'])
resultado = [proximo_char]

for i in range(1000):
    proximo_char, states = one_step_model.generate_one_step(proximo_char, states=states)
    resultado.append(proximo_char)

resultado = tf.strings.join(resultado)
fim = time.time()
print(resultado[0].numpy().decode('utf-8'), '\n\n' + '_' * 80)
print('\nRun time: ', fim - start)

# EXPORTAR O MODELO (SALVAR)
# este modelo de etapa única pode ser salvo para ser utilizado em qualquer lugar

tf.saved_model.save(one_step_model, 'one_step')