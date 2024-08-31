#include <json-c/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *inputString(FILE *fp, size_t size);
json_object *get_json_inputs();
const char *get_json_value(json_object *json, char *key);
char *encrypt(const char *msg);
char *decrypt(char *msg);

int main(int argc, const char *argv[]) {
  json_object *inputs = get_json_inputs();
  const char *msg = get_json_value(inputs, "plaintext");

  char *cipher = encrypt(msg);

  json_object *outputs = json_object_new_object();
  json_object_object_add(outputs, "algorithm", json_object_new_string("same"));
  json_object_object_add(outputs, "ciphertext", json_object_new_string(cipher));

  fprintf(stdout, "%s",
          json_object_to_json_string_ext(outputs, JSON_C_TO_STRING_SPACED |
                                                      JSON_C_TO_STRING_PRETTY));

  // Decrypt
  // fprintf(stdout, "\n%s", decrypt(cipher));

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

  char *value_str_trim;
  if (value_str[0] == '"') {
    int n = strlen(value_str) - 2;
    value_str_trim = (char *)calloc(n + 1, sizeof(char));
    strncpy(value_str_trim, value_str + 1, n);
  } else {
    int n = strlen(value_str);
    value_str_trim = (char *)calloc(n + 1, sizeof(char));
    strncpy(value_str_trim, value_str, n);
  }

  return value_str_trim;
}

char *encrypt(const char *msg) {
  char *cipher = (char *)calloc(strlen(msg) + 1, sizeof(char));
  strcpy(cipher, msg);

  return cipher;
}

char *decrypt(char *cipher) {
  char *msg = (char *)calloc(strlen(cipher) + 1, sizeof(char));
  strcpy(msg, cipher);

  return msg;
}
