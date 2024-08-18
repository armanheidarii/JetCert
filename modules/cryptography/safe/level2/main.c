#include <ctype.h>
#include <json-c/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *inputString(FILE *fp, size_t size);
json_object *get_json_inputs();
const char *get_json_value(json_object *json, char *key);
int mod(int a, int b);
int ismisc1(char c);
int ismisc2(char c);
char *encrypt(const char *msg, int shift);
char *decrypt(char *msg, int shift);

int main(int argc, const char *argv[]) {
  json_object *inputs = get_json_inputs();
  const char *msg = get_json_value(inputs, "plaintext");

  int shift = 4;
  char *cipher = encrypt(msg, shift);

  json_object *outputs = json_object_new_object();
  json_object_object_add(outputs, "algorithm",
                         json_object_new_string("shift_cipher"));
  json_object_object_add(outputs, "ciphertext", json_object_new_string(cipher));

  fprintf(stdout, "%s",
          json_object_to_json_string_ext(outputs, JSON_C_TO_STRING_SPACED |
                                                      JSON_C_TO_STRING_PRETTY));

  // Decrypt
  // fprintf(stdout, "\n%s", decrypt(cipher, shift));

  free((void *)msg);
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

json_object *get_json_inputs() {
  char *inputs_str = inputString(stdin, 10);
  json_object *inputs = json_tokener_parse(inputs_str);
  return inputs;
}

const char *get_json_value(json_object *json, char *key) {
  json_object *value;

  json_object_object_get_ex(json, key, &value);

  const char *value_str = json_object_to_json_string(value);

  int n = strlen(value_str) - 2;
  char *value_str_trim = (char *)calloc(n + 1, sizeof(char));
  strncpy(value_str_trim, value_str + 1, n);

  return value_str_trim;
}

int mod(int a, int b) { return ((a % b) + b) % b; }

int ismisc1(char c) {
  char *misc1 = " !\"#$%&'()*+,-./";
  for (int i = 0; i < strlen(misc1); i++) {
    if (misc1[i] == c)
      return 1;
  }

  return 0;
}

int ismisc2(char c) {
  char *misc2 = ":;<=>?@";
  for (int i = 0; i < strlen(misc2); i++) {
    if (misc2[i] == c)
      return 1;
  }

  return 0;
}

char *encrypt(const char *msg, int shift) {
  int size = strlen(msg);
  char *cipher = (char *)calloc(size + 1, sizeof(char));

  // Traverse Text
  for (int i = 0; i < size; i++) {
    // apply transformation to each character

    // Encrypt First Group of Misc Letters
    if (ismisc1(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 32) % 16 + 32);

    // Encrypt Second Group of Misc Letters
    else if (ismisc2(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 58) % 7 + 58);

    // Encrypt Digit Letters
    else if (isdigit(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 48) % 10 + 48);

    // Encrypt Uppercase Letters
    else if (isupper(msg[i]))
      cipher[i] = (char)((int)(msg[i] + shift - 65) % 26 + 65);

    // Encrypt Lowercase Letters
    else
      cipher[i] = (char)((int)(msg[i] + shift - 97) % 26 + 97);
  }

  // Return the resulting string
  return cipher;
}

char *decrypt(char *cipher, int shift) {
  int size = strlen(cipher);
  char *msg = (char *)calloc(size + 1, sizeof(char));

  // Traverse Text
  for (int i = 0; i < size; i++) {
    // apply transformation to each character

    // Encrypt First Group of Misc Letters
    if (ismisc1(cipher[i]))
      msg[i] = (char)(mod((int)(cipher[i] - shift - 32), 16) + 32);

    // Encrypt Second Group of Misc Letters
    else if (ismisc2(cipher[i]))
      msg[i] = (char)(mod((int)(cipher[i] - shift - 58), 7) + 58);

    // Encrypt Digit Letters
    else if (isdigit(cipher[i]))
      msg[i] = (char)(mod((int)(cipher[i] - shift - 48), 10) + 48);

    // Encrypt Uppercase Letters
    else if (isupper(cipher[i]))
      msg[i] = (char)(mod((int)(cipher[i] - shift - 65), 26) + 65);

    // Encrypt Lowercase Letters
    else
      msg[i] = (char)(mod((int)(cipher[i] - shift - 97), 26) + 97);
  }

  // Return the resulting string
  return msg;
}
