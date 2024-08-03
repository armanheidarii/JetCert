#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int shift = 4;

char *inputString(FILE *fp, size_t size);
int mod(int a, int b);
char *encrypt(char *msg, int shift);
char *decrypt(char *msg, int shift);

int main(int argc, const char *argv[]) {
  char *msg = inputString(stdin, 10);

  char *cipher = encrypt(msg, shift);
  printf("%s\n", cipher);

  // Decrypt
  // printf("\n%s", decrypt(cipher, shift));

  free(msg);
  free(cipher);

  return 0;
}

char *inputString(FILE *fp, size_t size) {
  char *str;
  int ch;
  size_t len = 0;
  str = realloc(NULL, sizeof(*str) * size);
  if (!str)
    return str;
  while (EOF != (ch = fgetc(fp)) && ch != '\n') {
    str[len++] = ch;
    if (len == size) {
      str = realloc(str, sizeof(*str) * (size += 16));
      if (!str)
        return str;
    }
  }
  str[len++] = '\0';

  return realloc(str, sizeof(*str) * len);
}

int mod(int a, int b) { return ((a % b) + b) % b; }

char *encrypt(char *msg, int shift) {
  int size = strlen(msg);
  char *cipher = (char *)malloc(sizeof(char) * size);

  // Traverse Text
  for (int i = 0; i < size; i++) {
    // apply transformation to each character

    // Encrypt Digit letters
    if (isdigit(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 48) % 10 + 48);

    // Encrypt Uppercase letters
    else if (isupper(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 65) % 26 + 65);

    // Encrypt Lowercase letters
    else
      cipher[i] = (char)((int)(msg[i] + shift - 97) % 26 + 97);
  }

  // Return the resulting string
  return cipher;
}

char *decrypt(char *msg, int shift) {
  int size = strlen(msg);
  char *cipher = (char *)malloc(sizeof(char) * size);

  // Traverse Text
  for (int i = 0; i < size; i++) {
    // apply transformation to each character

    // Encrypt Digit letters
    if (isdigit(msg[i]))
      cipher[i] = (char)(mod((int)(msg[i] - shift - 48), 10) + 48);

    // Encrypt Uppercase letters
    else if (isupper(msg[i]))
      cipher[i] = (char)(mod((int)(msg[i] - shift - 65), 26) + 65);

    // Encrypt Lowercase letters
    else
      cipher[i] = (char)(mod((int)(msg[i] - shift - 97), 26) + 97);
  }

  // Return the resulting string
  return cipher;
}
