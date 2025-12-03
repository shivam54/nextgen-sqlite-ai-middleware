#!/bin/bash
# Rebuild SQLite after making source code changes
# Use this after modifying pcache.c, pcache1.c, etc.

cd sqlite-src-3510000

echo "Rebuilding SQLite after source changes..."

# Recompile the core
echo "Compiling sqlite3.c..."
gcc -O2 -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION \
    -DSQLITE_ENABLE_FTS4 -DSQLITE_ENABLE_FTS5 \
    -I. -Isrc \
    -c sqlite3.c -o sqlite3.o

if [ $? -ne 0 ]; then
    echo "ERROR: Compilation failed! Check your changes."
    exit 1
fi

# Create a proper SQL shell (not just test version)
echo "Creating SQL shell..."
cat > sqlite3_shell.c << 'EOFSHELL'
#include "sqlite3.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
    int i;
    for(i=0; i<argc; i++){
        printf("%s = %s\n", azColName[i] ? azColName[i] : "NULL", 
               argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

int main(int argc, char **argv){
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;
    char *sql;

    if( argc==2 && strcmp(argv[1], "--version")==0 ){
        printf("%s\n", sqlite3_libversion());
        return 0;
    }

    if( argc!=3 ){
        fprintf(stderr, "Usage: %s DATABASE SQL-COMMAND\n", argv[0]);
        exit(1);
    }

    rc = sqlite3_open(argv[1], &db);
    if( rc ){
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return(1);
    }

    sql = argv[2];
    rc = sqlite3_exec(db, sql, callback, 0, &zErrMsg);
    if( rc!=SQLITE_OK ){
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    }

    sqlite3_close(db);
    return 0;
}
EOFSHELL

# Compile the shell
echo "Compiling shell..."
gcc -O2 -I. -Isrc -DSQLITE_CORE=1 -c sqlite3_shell.c -o sqlite3_shell.o

if [ $? -ne 0 ]; then
    echo "ERROR: Shell compilation failed!"
    exit 1
fi

# Compile ML scoring (if it exists)
if [ -f ml_scoring.c ]; then
    echo "Compiling ML scoring..."
    gcc -O2 -I. -Isrc -DSQLITE_CORE=1 -c ml_scoring.c -o ml_scoring.o
    
    if [ $? -eq 0 ]; then
        ML_OBJ="ml_scoring.o"
        echo "✓ ML scoring compiled"
    else
        echo "WARNING: ML scoring compilation failed, continuing without it"
        ML_OBJ=""
    fi
else
    echo "Note: ml_scoring.c not found, building without ML"
    ML_OBJ=""
fi

# Link
echo "Linking..."
if [ -n "$ML_OBJ" ]; then
    gcc -mconsole -o sqlite3.exe sqlite3.o sqlite3_shell.o $ML_OBJ
else
    gcc -mconsole -o sqlite3.exe sqlite3.o sqlite3_shell.o
fi

# Test
echo "Testing..."
./sqlite3.exe --version

if [ $? -eq 0 ]; then
    echo "✓ Rebuild successful!"
    echo "  Now sqlite3.exe can execute SQL commands"
else
    echo "ERROR: Rebuild failed!"
    exit 1
fi

