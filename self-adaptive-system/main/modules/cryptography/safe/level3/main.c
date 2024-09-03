#include <json-c/json.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LB32 0x00000001
#define LB64 0x0000000000000001
#define L64_MASK 0x00000000ffffffff
#define H64_MASK 0xffffffff00000000

/* Initial Permutation Table */
static char IP[] = {58, 50, 42, 34, 26, 18, 10, 2,  60, 52, 44, 36, 28,
                    20, 12, 4,  62, 54, 46, 38, 30, 22, 14, 6,  64, 56,
                    48, 40, 32, 24, 16, 8,  57, 49, 41, 33, 25, 17, 9,
                    1,  59, 51, 43, 35, 27, 19, 11, 3,  61, 53, 45, 37,
                    29, 21, 13, 5,  63, 55, 47, 39, 31, 23, 15, 7};

/* Inverse Initial Permutation Table */
static char PI[] = {40, 8,  48, 16, 56, 24, 64, 32, 39, 7,  47, 15, 55,
                    23, 63, 31, 38, 6,  46, 14, 54, 22, 62, 30, 37, 5,
                    45, 13, 53, 21, 61, 29, 36, 4,  44, 12, 52, 20, 60,
                    28, 35, 3,  43, 11, 51, 19, 59, 27, 34, 2,  42, 10,
                    50, 18, 58, 26, 33, 1,  41, 9,  49, 17, 57, 25};

/*Expansion Table */
static char E[] = {32, 1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
                   8,  9,  10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1};

/* Post S-Box permutation */
static char P[] = {16, 7, 20, 21, 29, 12, 28, 17, 1,  15, 23,
                   26, 5, 18, 31, 10, 2,  8,  24, 14, 32, 27,
                   3,  9, 19, 13, 30, 6,  22, 11, 4,  25};

/* The S-Box Table */
static char S[8][64] = {
    {/* S1 */
     14, 4,  13, 1, 2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0, 7,
     0,  15, 7,  4, 14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3, 8,
     4,  1,  14, 8, 13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5, 0,
     15, 12, 8,  2, 4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6, 13},
    {/* S2 */
     15, 1,  8,  14, 6,  11, 3,  4,  9,  7, 2,  13, 12, 0, 5,  10,
     3,  13, 4,  7,  15, 2,  8,  14, 12, 0, 1,  10, 6,  9, 11, 5,
     0,  14, 7,  11, 10, 4,  13, 1,  5,  8, 12, 6,  9,  3, 2,  15,
     13, 8,  10, 1,  3,  15, 4,  2,  11, 6, 7,  12, 0,  5, 14, 9},
    {/* S3 */
     10, 0,  9,  14, 6, 3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8,
     13, 7,  0,  9,  3, 4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1,
     13, 6,  4,  9,  8, 15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7,
     1,  10, 13, 0,  6, 9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12},
    {/* S4 */
     7,  13, 14, 3, 0,  6,  9,  10, 1,  2, 8, 5,  11, 12, 4,  15,
     13, 8,  11, 5, 6,  15, 0,  3,  4,  7, 2, 12, 1,  10, 14, 9,
     10, 6,  9,  0, 12, 11, 7,  13, 15, 1, 3, 14, 5,  2,  8,  4,
     3,  15, 0,  6, 10, 1,  13, 8,  9,  4, 5, 11, 12, 7,  2,  14},
    {/* S5 */
     2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0, 14, 9,
     14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9, 8,  6,
     4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3, 0,  14,
     11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4, 5,  3},
    {/* S6 */
     12, 1,  10, 15, 9, 2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11,
     10, 15, 4,  2,  7, 12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8,
     9,  14, 15, 5,  2, 8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6,
     4,  3,  2,  12, 9, 5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13},
    {/* S7 */
     4,  11, 2,  14, 15, 0, 8,  13, 3,  12, 9, 7,  5,  10, 6, 1,
     13, 0,  11, 7,  4,  9, 1,  10, 14, 3,  5, 12, 2,  15, 8, 6,
     1,  4,  11, 13, 12, 3, 7,  14, 10, 15, 6, 8,  0,  5,  9, 2,
     6,  11, 13, 8,  1,  4, 10, 7,  9,  5,  0, 15, 14, 2,  3, 12},
    {/* S8 */
     13, 2,  8,  4, 6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7,
     1,  15, 13, 8, 10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2,
     7,  11, 4,  1, 9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8,
     2,  1,  14, 7, 4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11}};

/* Permuted Choice 1 Table */
static char PC1[] = {57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
                     10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,

                     63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
                     14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4};

/* Permuted Choice 2 Table */
static char PC2[] = {14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
                     23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
                     41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};

/* Iteration Shift Array */
static char iteration_shift[] = {
    /* 1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16 */
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};

uint64_t key[3] = {0x9474B8E8C73BCA7D, 0x9474B8E8C73BCA7C, 0x9474B8E8C73BC97D};
uint64_t block_size = 16;

char *inputString(FILE *fp, size_t size);
json_object *get_json_inputs();
const char *get_json_value(json_object *json, char *key);
uint64_t hex_to_uint64(char *hex_str);
char *hex_to_ascii(char *hex_str);
char *ascii_to_hex(const char *msg);
char *trim_trailing_zeros(char *hex);
char *padding(char *msg_hex);
uint64_t des(uint64_t input, uint64_t key, char mode);
char *encrypt_block(char *msg_block, char mode);
char *encrypt_worker(const char *msg, char mode);
char *encrypt(const char *msg);
char *decrypt(char *cipher);

int main(int argc, const char *argv[]) {
  json_object *inputs = get_json_inputs();
  const char *msg = get_json_value(inputs, "plaintext");

  char *cipher = encrypt(msg);

  json_object *outputs = json_object_new_object();
  json_object_object_add(outputs, "algorithm", json_object_new_string("3_DES"));
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

uint64_t hex_to_uint64(char *hex_str) {
  size_t length = strlen(hex_str);

  // Check if the length of the hex string is valid for uint64_t (up to 16 hex
  // digits)
  if (length > 16) {
    printf("Hex string is too long to convert to uint64_t.\n");
    return 0;
  }

  uint64_t result = 0;

  // Convert each hex digit to its integer value and accumulate into result
  for (size_t i = 0; i < length; i++) {
    char c = hex_str[i];
    int value;

    if (c >= '0' && c <= '9') {
      value = c - '0';
    } else if (c >= 'a' && c <= 'f') {
      value = 10 + (c - 'a');
    } else if (c >= 'A' && c <= 'F') {
      value = 10 + (c - 'A');
    } else {
      printf("Invalid character in hex string: %c\n", c);
      return 0;
    }

    result = (result << 4) | value;
  }

  return result;
}

char *hex_to_ascii(char *hex_str) {
  size_t length = strlen(hex_str);
  char *ascii_str = (char *)calloc((length / 2) + 1, sizeof(char));
  if (length % 2 != 0) {
    printf("Invalid hex string length.\n");
    return NULL;
  }

  for (size_t i = 0; i < length; i += 2) {
    char hex_byte[3];
    hex_byte[0] = hex_str[i];
    hex_byte[1] = hex_str[i + 1];
    hex_byte[2] = '\0';

    ascii_str[i / 2] = (char)strtol(hex_byte, NULL, 16);
  }
  ascii_str[length / 2] = '\0';

  return ascii_str;
}

// function to convert ascii char* to hex-string (char*)
char *ascii_to_hex(const char *msg) {
  int len = strlen(msg);
  char *msg_hex = (char *)calloc((len * 2) + 1, sizeof(char));

  int loop;
  int i;

  i = 0;
  loop = 0;

  while (msg[loop] != '\0') {
    sprintf((char *)(msg_hex + i), "%02X", msg[loop]);
    loop += 1;
    i += 2;
  }
  // insert NULL at the end of the output string
  msg_hex[i++] = '\0';

  return msg_hex;
}

char *trim_trailing_zeros(char *hex) {
  int len = strlen(hex);
  while (len >= 2 && hex[len - 1] == '0' && hex[len - 2] == '0') {
    hex[len - 1] = '\0';
    hex[len - 2] = '\0';
    len -= 2;
  }
  return hex;
}

char *padding(char *msg_hex) {
  int msg_hex_len = strlen(msg_hex);
  if (msg_hex_len % block_size == 0)
    return msg_hex;

  int padding_len = block_size - (msg_hex_len % block_size);
  char *msg_padding =
      (char *)calloc((msg_hex_len + padding_len) + 1, sizeof(char));
  strcpy(msg_padding, msg_hex);

  for (int i = 0; i < padding_len; i++)
    strcat(msg_padding, "0");

  return msg_padding;
}

uint64_t des(uint64_t input, uint64_t key, char mode) {

  int i, j;

  /* 8 bit */
  char satir, sutun;

  /* 28 bits */
  uint32_t C = 0;
  uint32_t D = 0;

  /* 32 bit */
  uint32_t L = 0;
  uint32_t R = 0;
  uint32_t s_output = 0;
  uint32_t f_function_res = 0;
  uint32_t temp = 0;

  /* 48 bit */
  uint64_t sub_key[16] = {0};
  uint64_t s_input = 0;

  /* 56 bit */
  uint64_t permuted_choice_1 = 0;
  uint64_t permuted_choice_2 = 0;

  /* 64 bit */
  uint64_t init_perm_res = 0;
  uint64_t inv_init_perm_res = 0;
  uint64_t pre_output = 0;

  /* Initial Permutation */
  for (i = 0; i < 64; i++) {

    init_perm_res <<= 1;
    init_perm_res |= (input >> (64 - IP[i])) & LB64;
  }
  L = (uint32_t)(init_perm_res >> 32) & L64_MASK;
  R = (uint32_t)init_perm_res & L64_MASK;

  /* Initial Key Mixing */
  for (i = 0; i < 56; i++) {

    permuted_choice_1 <<= 1; //
    permuted_choice_1 |= (key >> (64 - PC1[i])) & LB64;
  }

  C = (uint32_t)((permuted_choice_1 >> 28) & 0x000000000fffffff);
  D = (uint32_t)(permuted_choice_1 & 0x000000000fffffff);

  for (i = 0; i < 16; i++) {
    for (j = 0; j < iteration_shift[i]; j++) {

      C = 0x0fffffff & (C << 1) | 0x00000001 & (C >> 27);
      D = 0x0fffffff & (D << 1) | 0x00000001 & (D >> 27);
    }

    permuted_choice_2 = 0;
    permuted_choice_2 = (((uint64_t)C) << 28) | (uint64_t)D;

    sub_key[i] = 0;

    for (j = 0; j < 48; j++) {
      sub_key[i] <<= 1;
      sub_key[i] |= (permuted_choice_2 >> (56 - PC2[j])) & LB64;
    }
  }

  for (i = 0; i < 16; i++) {

    s_input = 0;

    for (j = 0; j < 48; j++) {
      s_input <<= 1;
      s_input |= (uint64_t)((R >> (32 - E[j])) & LB32);
    }

    if (mode == 'd') {
      // Decryption
      s_input = s_input ^ sub_key[15 - i];

    } else {
      // Encryption
      s_input = s_input ^ sub_key[i];
    }

    for (j = 0; j < 8; j++) {

      satir = (char)((s_input & (0x0000840000000000 >> 6 * j)) >> (42 - 6 * j));
      satir = (satir >> 4) | satir & 0x01;

      sutun = (char)((s_input & (0x0000780000000000 >> 6 * j)) >> (43 - 6 * j));

      s_output <<= 4;
      s_output |= (uint32_t)(S[j][16 * satir + sutun] & 0x0f);
    }

    f_function_res = 0;

    for (j = 0; j < 32; j++) {

      f_function_res <<= 1;
      f_function_res |= (s_output >> (32 - P[j])) & LB32;
    }

    temp = R;
    R = L ^ f_function_res;
    L = temp;
  }

  pre_output = (((uint64_t)R) << 32) | (uint64_t)L;

  /* Inverse Initial Permutation */
  for (i = 0; i < 64; i++) {

    inv_init_perm_res <<= 1;
    inv_init_perm_res |= (pre_output >> (64 - PI[i])) & LB64;
  }

  return inv_init_perm_res;
}

char *encrypt_block(char *msg_block, char mode) {
  uint64_t input = hex_to_uint64(msg_block);
  uint64_t result = input;

  uint64_t key0 = mode == 'e' ? key[0] : key[2];
  uint64_t key1 = key[1];
  uint64_t key2 = mode == 'e' ? key[2] : key[0];

  char mode0 = mode;
  char mode1 = mode == 'e' ? 'd' : 'e';
  char mode2 = mode;

  result = des(input, key0, mode0);
  result = des(result, key1, mode1);
  result = des(result, key2, mode2);

  char *result_str = (char *)calloc(block_size + 1, sizeof(char));
  sprintf(result_str, "%016lx", result);

  return result_str;
}

char *encrypt_worker(const char *msg, char mode) {
  char *msg_hex = (char *)calloc(strlen(msg) + 1, sizeof(char));
  strcpy(msg_hex, msg);

  if (mode == 'e')
    msg_hex = ascii_to_hex(msg);

  char *msg_padding = padding(msg_hex);

  char *cipher = (char *)calloc(strlen(msg_padding) + 1, sizeof(char));

  char *msg_block = (char *)calloc(block_size + 1, sizeof(char));
  for (int i = 0; i < strlen(msg_padding); i += block_size) {
    strncpy(msg_block, msg_padding + i, block_size);
    strcat(cipher, encrypt_block(msg_block, mode));
  }

  if (mode == 'd')
    cipher = hex_to_ascii(trim_trailing_zeros(cipher));

  return cipher;
}

char *encrypt(const char *msg) { return encrypt_worker(msg, 'e'); }

char *decrypt(char *cipher) { return encrypt_worker(cipher, 'd'); }