#include "../../../../tools/cJSON/cJSON.h"
#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int query_len = 1024;

int id_len = 50;
int public_id_len = 50;
int name_len = 100;
int email_len = 70;
int password_len = 80;

char db_path[] = "/home/arman/develop/compiler-artifact/jetCert/db/instance/"
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
cJSON *get_json_inputs();
static int callback(void *data, int argc, char **argv, char **azColName);

int main(int argc, char *argv[]) {
  sqlite3 *db;
  char *zErrMsg = 0;
  int rc;
  char *sql = malloc(query_len * sizeof(char));
  const char *data = "Callback function called";

  /* Open database */
  rc = sqlite3_open(db_path, &db);
  if (rc) {
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    return 1;
  }

  cJSON *inputs = get_json_inputs();
  cJSON *outputs = cJSON_CreateObject();

  char *email;
  cJSON *email_json = cJSON_GetObjectItemCaseSensitive(inputs, "email");
  if (cJSON_IsString(email_json) && (email_json->valuestring != NULL))
    email = email_json->valuestring;

  if (strlen(email) > email_len) {
    cJSON_AddFalseToObject(outputs, "login");
    fprintf(stdout, "%s", cJSON_Print(outputs));
    fprintf(stderr, "Your email is invalid!");
    return 0;
  }

  char *password;
  cJSON *password_json = cJSON_GetObjectItemCaseSensitive(inputs, "password");
  if (cJSON_IsString(password_json) && (password_json->valuestring != NULL))
    password = password_json->valuestring;

  if (strlen(password) > password_len) {
    cJSON_AddFalseToObject(outputs, "login");
    fprintf(stdout, "%s", cJSON_Print(outputs));
    fprintf(stderr, "Your password is invalid!");
    return 0;
  }

  /* Create SQL statement */
  sprintf(sql, "SELECT * from USER WHERE email = \"%s\"", email);

  /* Execute SQL statement */
  rc = sqlite3_exec(db, sql, callback, (void *)data, &zErrMsg);

  if (rc != SQLITE_OK) {
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
    sqlite3_free(zErrMsg);
    return 1;
  } else {
    if (!user) {
      cJSON_AddFalseToObject(outputs, "login");
      fprintf(stdout, "%s", cJSON_Print(outputs));
      fprintf(stderr, "The user with the given email address was not found!");
      return 0;
    }

    if (strcmp(user->password, password)) {
      cJSON_AddFalseToObject(outputs, "login");
      fprintf(stdout, "%s", cJSON_Print(outputs));
      fprintf(stderr, "Your password was not match!");
      return 0;
    }

    cJSON_AddTrueToObject(outputs, "login");
    fprintf(stdout, "%s", cJSON_Print(outputs));
  }

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

cJSON *get_json_inputs() {
  char *buffer = inputString(stdin, 10);
  cJSON *json = cJSON_Parse(buffer);
  if (json == NULL) {
    const char *error_ptr = cJSON_GetErrorPtr();
    if (error_ptr != NULL) {
      fprintf(stderr, "Error: %s\n", error_ptr);
    }
    cJSON_Delete(json);
    exit(1);
  }
  return json;
}

static int callback(void *data, int argc, char **argv, char **azColName) {
  if (argc > 0) {
    user = (struct User *)malloc(sizeof(struct User));

    user->id = malloc(id_len * sizeof(char));
    strcpy(user->id, argv[0]);

    user->public_id = malloc(public_id_len * sizeof(char));
    strcpy(user->public_id, argv[1]);

    user->name = malloc(name_len * sizeof(char));
    strcpy(user->name, argv[2]);

    user->email = malloc(email_len * sizeof(char));
    strcpy(user->email, argv[3]);

    user->password = malloc(password_len * sizeof(char));
    strcpy(user->password, argv[4]);
  }

  return 0;
}
