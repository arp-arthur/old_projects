def train(model, dataset, checkpoint_callback):
    EPOCHS = 20

    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])



