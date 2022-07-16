import tensorflow as tf

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
