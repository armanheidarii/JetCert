#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long int n, e, d;
long int msg_size;

char *inputString(FILE *fp, size_t size);
int prime(long int);
void generate_e(long int, long int);
long int generate_d(long int, long int);
void generate_keys();
long int *encrypt(char *msg);
void print_cipher(long int *en);
long int *decrypt(long int *);
void print_msg(long int *msg);

int main() {
  generate_keys();

  char *msg = inputString(stdin, 10);

  long int *cipher = encrypt(msg);
  print_cipher(cipher);
  printf("%ld\n", n);
  printf("%ld\n", d);

  // Decrypt
  // print_msg(decrypt(cipher));

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

long int *encrypt(char *msg) {
  msg_size = strlen(msg);
  long int *cipher = (long int *)malloc(sizeof(long int) * msg_size);

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

void print_cipher(long int *cipher) {
  for (long int i = 0; i < msg_size - 1; i++)
    printf("%ld_", cipher[i]);
  printf("%ld\n", cipher[msg_size - 1]);
}

long int *decrypt(long int *cipher) {
  long int *m = (long int *)malloc(sizeof(long int) * msg_size);

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

void print_msg(long int *msg) {
  for (long int i = 0; i < msg_size; i++)
    printf("%c", (char)msg[i]);
  printf("\n");
}
