#include "../../../../tools/cJSON/cJSON.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *inputString(FILE *fp, size_t size);
cJSON *get_json_inputs();
char *encrypt(char *msg);
char *decrypt(char *cipher);

int main(int argc, const char *argv[]) {
  cJSON *json = get_json_inputs();
  char *msg = cJSON_GetObjectItemCaseSensitive(json, "plaintext")->valuestring;

  char *cipher = encrypt(msg);
  printf("%s\n", cipher);

  // Decrypt
  // printf("%s", decrypt(cipher));

  cJSON_Delete(json);
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

cJSON *get_json_inputs() {
  char *buffer = inputString(stdin, 10);
  cJSON *json = cJSON_Parse(buffer);
  if (json == NULL) {
    const char *error_ptr = cJSON_GetErrorPtr();
    if (error_ptr != NULL) {
      printf("Error: %s\n", error_ptr);
    }
    cJSON_Delete(json);
    exit(1);
  }
  return json;
}

char *encrypt(char *msg) {
  char *cipher = (char *)malloc(sizeof(char) * strlen(msg));
  strcpy(cipher, msg);

  return cipher;
}

char *decrypt(char *cipher) {
  char *msg = (char *)malloc(sizeof(char) * strlen(cipher));
  strcpy(msg, cipher);

  return msg;
}
