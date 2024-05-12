# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from tensorflow.keras import layers, models

# # Load the data
# data = pd.read_csv('/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Admission_Predict_Ver1.1.csv')

# # Normalize the data
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# scaled_data = scaler.fit_transform(data.drop(['Serial No.'], axis=1))

# # GAN components
# def build_generator(latent_dim, output_dim):
#     model = models.Sequential([
#         layers.Dense(128, activation='relu', input_dim=latent_dim),
#         layers.Dense(output_dim, activation='sigmoid')
#     ])
#     return model

# def build_discriminator(input_dim):
#     model = models.Sequential([
#         layers.Dense(128, activation='relu', input_dim=input_dim),
#         layers.Dense(1, activation='sigmoid')

#     ])
#     return model

# latent_dim = 100
# generator = build_generator(latent_dim, scaled_data.shape[1])
# discriminator = build_discriminator(scaled_data.shape[1])
# discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# # Combined network
# discriminator.trainable = False
# gan_input = layers.Input(shape=(latent_dim,))
# x = generator(gan_input)
# gan_output = discriminator(x)
# gan = models.Model(gan_input, gan_output)
# gan.compile(optimizer='adam', loss='binary_crossentropy')

# # Training
# def train_gan(generator, discriminator, gan, scaled_data, epochs, batch_size, latent_dim):
#     for epoch in range(epochs):
#         # Select a random batch of samples
#         idx = np.random.randint(0, scaled_data.shape[0], batch_size)
#         real_data = scaled_data[idx]

#         # Generate fake data
#         noise = np.random.normal(0, 1, (batch_size, latent_dim))
#         fake_data = generator.predict(noise)

#         # Train the discriminator
#         d_loss_real = discriminator.train_on_batch(real_data, np.ones((batch_size, 1)))
#         d_loss_fake = discriminator.train_on_batch(fake_data, np.zeros((batch_size, 1)))
#         d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

#         # Train the generator
#         noise = np.random.normal(0, 1, (batch_size, latent_dim))
#         g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

#         if epoch % 100 == 0:
#             print(f'Epoch: {epoch} Discriminator Loss: {d_loss} Generator Loss: {g_loss}')

# epochs = 10000
# batch_size = 32
# train_gan(generator, discriminator, gan, scaled_data, epochs, batch_size, latent_dim)

# # Generating new data
# def generate_data(generator, num_samples, latent_dim):
#     noise = np.random.normal(0, 1, (num_samples, latent_dim))
#     generated_data = generator.predict(noise)
#     generated_data = scaler.inverse_transform(generated_data)
#     return pd.DataFrame(generated_data, columns=data.columns[1:])

# new_data = generate_data(generator, 19500, latent_dim)
# print(new_data.head())

# # Append and save the new dataset
# final_data = pd.concat([data, new_data]).reset_index(drop=True)
# final_data.to_csv('Expanded_Admission_Predict.csv', index=False)

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

# Load the data
data = pd.read_csv('/Users/jiaxinliu/Desktop/FlashSMPEvaluation/DataSets/ADM/app/Admission_Predict_Ver1.1.csv')

# Normalize the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data.drop(['Serial No.'], axis=1))

# GAN components
def build_generator(latent_dim, output_dim):
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_dim=latent_dim),
        layers.Dense(output_dim, activation='sigmoid')
    ])
    return model

def build_discriminator(input_dim):
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_dim=input_dim),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

latent_dim = 100
generator = build_generator(latent_dim, scaled_data.shape[1])
discriminator = build_discriminator(scaled_data.shape[1])
discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Combined network
discriminator.trainable = False
gan_input = layers.Input(shape=(latent_dim,))
x = generator(gan_input)
gan_output = discriminator(x)
gan = models.Model(gan_input, gan_output)
gan.compile(optimizer='adam', loss='binary_crossentropy')

# Training
def train_gan(generator, discriminator, gan, scaled_data, epochs, batch_size, latent_dim):
    for epoch in tqdm(range(epochs), desc="Training Progress"):
        # Select a random batch of samples
        idx = np.random.randint(0, scaled_data.shape[0], batch_size)
        real_data = scaled_data[idx]

        # Generate fake data
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        fake_data = generator.predict(noise)

        # Train the discriminator
        d_loss_real = discriminator.train_on_batch(real_data, np.ones((batch_size, 1)))
        d_loss_fake = discriminator.train_on_batch(fake_data, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Train the generator
        g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

        # Optionally print detailed progress
        if epoch % 100 == 0:
            print(f'Epoch: {epoch} / {epochs} - Disc Loss: {d_loss}, Gen Loss: {g_loss}')

epochs = 10000
batch_size = 32
train_gan(generator, discriminator, gan, scaled_data, epochs, batch_size, latent_dim)

# Generating new data
def generate_data(generator, num_samples, latent_dim):
    print("Generating data...")
    noise = np.random.normal(0, 1, (num_samples, latent_dim))
    generated_data = generator.predict(noise)
    generated_data = scaler.inverse_transform(generated_data)
    return pd.DataFrame(generated_data, columns=data.columns[1:])

new_data = generate_data(generator, 19500, latent_dim)
print(new_data.head())

# Append and save the new dataset
final_data = pd.concat([data, new_data]).reset_index(drop=True)
final_data.to_csv('Expanded_Admission_Predict.csv', index=False)
