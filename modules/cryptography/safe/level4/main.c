#include <json-c/json.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LONG_INT_STR_LEN 12

long int n, e, d;
long int msg_size;

char *inputString(FILE *fp, size_t size);
json_object *get_json_inputs();
const char *get_json_value(json_object *json, char *key);
int prime(long int);
void generate_e(long int, long int);
long int generate_d(long int, long int);
void generate_keys();
long int *encrypt(const char *msg);
long int *decrypt(long int *cipher);
char *cipher_str(long int *cipher);
char *msg_str(long int *msg);

int main(int argc, const char *argv[]) {
  generate_keys();

  json_object *inputs = get_json_inputs();
  const char *msg = get_json_value(inputs, "plaintext");

  long int *cipher = encrypt(msg);

  json_object *outputs = json_object_new_object();
  json_object_object_add(outputs, "algorithm", json_object_new_string("RSA"));
  json_object_object_add(outputs, "ciphertext",
                         json_object_new_string(cipher_str(cipher)));
  json_object_object_add(outputs, "n", json_object_new_int(n));
  json_object_object_add(outputs, "d", json_object_new_int(d));

  fprintf(stdout, "%s",
          json_object_to_json_string_ext(outputs, JSON_C_TO_STRING_SPACED |
                                                      JSON_C_TO_STRING_PRETTY));

  // Decrypt
  // fprintf(stdout, "\n%s", msg_str(decrypt(cipher)));

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

int prime(long int pr) {
  for (long int i = 2; i <= sqrt(pr); i++) {
    if (pr % i == 0)
      return 0;
  }
  return 1;
}

void generate_e(long int p, long int q) {
  long int t = (p - 1) * (q - 1);

  for (long int i = 2; i < t; i++) {
    if (t % i == 0)
      continue;

    if (prime(i) == 1 && i != p && i != q) {
      e = i;
      long int pot_d = generate_d(e, t);
      if (pot_d > 0) {
        d = pot_d;
        return;
      }
    }
  }
}

long int generate_d(long int x, long int t) {
  long int k = 1;
  while (1) {
    k += t;
    if (k % x == 0)
      return (k / x);
  }
}

void generate_keys() {
  long int p = 419, q = 541;
  if (!prime(p) || !prime(q)) {
    exit(1);
  }

  n = p * q;

  generate_e(p, q);
}

long int *encrypt(const char *msg) {
  msg_size = strlen(msg);
  long int *cipher = (long int *)malloc(msg_size * sizeof(long int));

  for (int i = 0; i < msg_size; i++) {
    long int k = 1;
    for (long int j = 0; j < e; j++) {
      k *= (msg[i] - 96);
      k %= n;
    }
    cipher[i] = k + 96;
  }
  return cipher;
}

char *cipher_str(long int *cipher) {
  char *cipher_cpy =
      (char *)calloc(LONG_INT_STR_LEN * msg_size + 1, sizeof(char));

  for (long int i = 0; i < msg_size; i++) {
    char *number_cpy = (char *)calloc(LONG_INT_STR_LEN + 1, sizeof(char));

    sprintf(number_cpy, "%ld", cipher[i]);

    if (i < msg_size - 1)
      strcat(number_cpy, "_");

    strcat(cipher_cpy, number_cpy);
  }

  return cipher_cpy;
}

long int *decrypt(long int *cipher) {
  long int *m = (long int *)calloc(msg_size + 1, sizeof(long int));

  for (int i = 0; i < msg_size; i++) {
    long int k = 1;
    for (long int j = 0; j < d; j++) {
      k *= cipher[i] - 96;
      k %= n;
    }
    m[i] = k + 96;
  }
  return m;
}

char *msg_str(long int *msg) {
  char *msg_cpy = (char *)calloc(msg_size + 1, sizeof(char));

  for (long int i = 0; i < msg_size; i++) {
    char c = (char)msg[i];
    char *cStr = malloc(sizeof(char));
    *cStr = c;
    strcat(msg_cpy, cStr);
  }

  return msg_cpy;
}
