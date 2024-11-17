// #include "../../../../tools/C-Simple-JSON-Parser/json.h"
#include <json-c/json.h>
#include <json-c/json_object.h>
#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>




#define FALSE 0
#define TRUE 1

int query_len = 1024;

int id_len = 50;
int public_id_len = 50;
int name_len = 100;
int email_len = 70;
int password_len = 80;

char db_path[] = "/home/arman/develop/compiler-artifact/jetCert/"
                 "self-adaptive-system/main/db/data/"
                 "Database.db";

struct User *user;

struct User {
  char *id;
  char *public_id;
  char *name;
  char *email;
  char *password;
};

char *inputString(FILE *fp, size_t size);
json_object *get_json_inputs();
const char *get_json_value(json_object *json, char *key);
static int callback(void *data, int argc, char **argv, char **azColName);

int main(int argc, char *argv[]) {
  sqlite3 *db;
  char *zErrMsg = 0;
  int rc;
  char *sql = calloc(query_len + 1, sizeof(char));
  const char *data = "Callback function called";

  /* Open database */
  rc = sqlite3_open(db_path, &db);
  if (rc) {
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    return 1;
  }

  json_object *inputs = get_json_inputs();
  json_object *outputs = json_object_new_object();

  const char *email = get_json_value(inputs, "email");

  if (strlen(email) > email_len) {
    json_object_object_add(outputs, "login", json_object_new_boolean(FALSE));
    fprintf(stdout, "%s", json_object_to_json_string(outputs));
    fprintf(stderr, "Your email is invalid!");
    return 0;
  }

  const char *password = get_json_value(inputs, "password");

  if (strlen(password) > password_len) {
    json_object_object_add(outputs, "login", json_object_new_boolean(FALSE));
    fprintf(stdout, "%s", json_object_to_json_string(outputs));
    fprintf(stderr, "Your password is invalid!");
    return 0;
  }

  /* Create SQL statement */
  sprintf(sql, "SELECT * from User WHERE Email = \"%s\"", email);

  /* Execute SQL statement */
  rc = sqlite3_exec(db, sql, callback, (void *)data, &zErrMsg);

  if (rc != SQLITE_OK) {
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
    sqlite3_free(zErrMsg);
    return 1;
  }

  if (!user) {
    json_object_object_add(outputs, "login", json_object_new_boolean(FALSE));
    fprintf(stdout, "%s", json_object_to_json_string(outputs));
    fprintf(stderr, "The user with the given email address was not found!");
    return 0;
  }

  if (strcmp(user->password, password)) {
    json_object_object_add(outputs, "login", json_object_new_boolean(FALSE));
    fprintf(stdout, "%s", json_object_to_json_string(outputs));
    fprintf(stderr, "Your password was not match!");
    return 0;
  }

  json_object_object_add(outputs, "login", json_object_new_boolean(TRUE));
  fprintf(stdout, "%s",
          json_object_to_json_string_ext(outputs, JSON_C_TO_STRING_SPACED |
                                                      JSON_C_TO_STRING_PRETTY));

  sqlite3_close(db);
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

static int callback(void *data, int argc, char **argv, char **azColName) {
  if (argc > 0) {
    user = (struct User *)malloc(sizeof(struct User));

    user->id = calloc(id_len + 1, sizeof(char));
    strcpy(user->id, argv[0]);

    user->public_id = calloc(public_id_len + 1, sizeof(char));
    strcpy(user->public_id, argv[1]);

    user->name = calloc(name_len + 1, sizeof(char));
    strcpy(user->name, argv[2]);

    user->email = calloc(email_len + 1, sizeof(char));
    strcpy(user->email, argv[3]);

    user->password = calloc(password_len + 1, sizeof(char));
    strcpy(user->password, argv[4]);
  }

  return 0;
}
