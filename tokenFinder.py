import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")
print("vocab_size:", encoder.n_vocab)

text = "Hello, world! This is a test string to count tokens."
tokens = encoder.encode(text)
print("Tokens:", tokens)


my_token = [13225, 11, 2375, 0, 1328, 382, 261, 1746, 1621, 316, 3605, 20290, 13]
decoded_text = encoder.decode(my_token)
print("Decoded text:", decoded_text)
print("Decoded text length:", len(decoded_text))