from __future__ import unicode_literals


import re
from os.path import splitext
from reviewbot.tools import Tool


class LiquibaseTool(Tool):
    """Review Bot tool to check XML of liquibase."""

    name = 'liquibase'
    version = '1.0'
    description = ('Checks if Liquibase-XML is valid')
    timeout = 30
    options = [
        {
              'name': 'AttributesToCheck',
              'field_type': 'django.forms.CharField',
              'default': ('tableName,name,constraintName,'
                          'indexName,columnName'),
              'field_options': {
                  'label': 'Attributes to check',
                  'help_text': 'Comma-separated list of \
                                attributes to search for',
                  'required': True,
                  },
        },
        {
              'name': 'MaxLength',
              'field_type': 'django.forms.CharField',
              'default': '30',
              'field_options': {
                  'label': 'Max length of attributes',
                  'help_text': 'Max length of attributesvalues in XML Files',
                  'required': True,
              },
        },
        {
            'name': 'LiquibaseHeaderRegex',
            'field_type': 'django.forms.CharField',
            'default': '.*<databaseChangeLog.*',
            'field_options': {
                'label': 'RegEx for Liquibase XML file header',
                'help_text': 'RegEx to identify a liquibase file',
                'required': True,
                },
        },
        {
            'name': 'ReservedWords',
            'field_type': 'django.forms.CharField',
            'default': 'ACCESS,ELSE,MODIFY,START,ADD,EXCLUSIVE,NOAUDIT, \
SELECT,ALL,EXISTS,NOCOMPRESS,SESSION,ALTER,FILE,NOT,SET,AND,FLOAT,NOTFOUND, \
SHARE,ANY,FOR,NOWAIT,SIZE,ARRAYLEN,FROM,NULL,SMALLINT,AS,GRANT,NUMBER,SQLBUF,\
ASC,GROUP,OF,SUCCESSFUL,AUDIT,HAVING,OFFLINE,SYNONYM,BETWEEN,IDENTIFIED,ON, \
SYSDATE,BY,IMMEDIATE,ONLINE,TABLE,CHAR,IN,OPTION,THEN,CHECK,INCREMENT,OR,TO,\
CLUSTER,INDEX,ORDER,TRIGGER,COLUMN,INITIAL,PCTFREE,UID,COMMENT,INSERT,PRIOR,\
UNION,COMPRESS,INTEGER,PRIVILEGES,UNIQUE,CONNECT,INTERSECT,PUBLIC,UPDATE,\
CREATE,INTO,RAW,USER,CURRENT,IS,RENAME,VALIDATE,DATE,LEVEL,RESOURCE,VALUES,\
DECIMAL,LIKE,REVOKE,VARCHAR,DEFAULT,LOCK,ROW,VARCHAR2,DELETE,LONG,ROWID,VIEW,\
DESC,MAXEXTENTS,ROWLABEL,WHENEVER,DISTINCT,MINUS,ROWNUM,WHERE,DROP,MODE,ROWS,\
WITH,ABORT,CRASH,DIGITS,ACCEPT,BINARY_INTEGER,DISPOSE,BODY,BOOLEAN,CURRVAL,DO,\
CURSOR,CASE,DATABASE,DATA_BASE,ELSIF,CHAR_BASE,END,ARRAY,DBA,ENTRY,CLOSE,\
DEBUGOFF,EXCEPTION,DEBUGON,EXCEPTION_INIT,CLUSTERS,DECLARE,ASSERT,COLAUTH,\
EXIT,ASSIGN,COLUMNS,FALSE,AT,COMMIT,DEFINITION,FETCH,AUTHORIZATION,DELAY,AVG,\
BASE_TABLE,CONSTANT,DELTA,FORM,BEGIN,COUNT,FUNCTION,NEW,RELEASE,SUM,GENERIC,\
NEXTVAL,REMR,TABAUTH,GOTO,TABLES,RETURN,TASK,REVERSE,TERMINATE,NUMBER_BASE,\
IF,ROLLBACK,TRUE,OPEN,TYPE,INDEXES,INDICATOR,ROWTYPE,RUN,OTHERS,SAVEPOINT,\
USE,OUT,SCHEMA,PACKAGE,PARTITION,SEPARATE,VARIANCE,POSITIVE,LIMITED,PRAGMA,\
VIEWS,LOOP,SPACE,WHEN,MAX,PRIVATE,SQL,MIN,PROCEDURE,SQLCODE,WHILE,SQLERRM,\
MLSLABEL,RAISE,WORK,MOD,RANGE,STATEMENT,XOR,REAL,STDDEV,NATURAL,RECORD,\
SUBTYPE,ACCESSIBLE,ANALYZE,ASENSITIVE,BEFORE,BIGINT,BINARY,BLOB,BOTH,CALL,\
CASCADE,CHANGE,CHARACTER,COLLATE,CONDITION,CONSTRAINT,CONTINUE,CONVERT,CROSS,\
CUBE,CUME_DIST,CURRENT_DATE,CURRENT_TIME,CURRENT_TIMESTAMP,CURRENT_USER,\
DATABASES,DAY_HOUR,DAY_MICROSECOND,DAY_MINUTE,DAY_SECOND,DEC,DELAYED,\
DENSE_RANK,DESCRIBE,DETERMINISTIC,DISTINCTROW,DIV,DOUBLE,DUAL,EACH,ELSEIF,\
EMPTY,ENCLOSED,ESCAPED,EXCEPT,EXPLAIN,FIRST_VALUE,FLOAT4,FLOAT8,FORCE,\
FOREIGN,FULLTEXT,GENERATED,GET,GROUPING,\
GROUPS,HIGH_PRIORITY,HOUR_MICROSECOND,\
HOUR_MINUTE,HOUR_SECOND,IGNORE,INFILE,INNER,INOUT,INSENSITIVE,INT,INT1,INT2,\
INT3,INT4,INT8,INTERVAL,IO_AFTER_GTIDS,IO_BEFORE_GTIDS,ITERATE,JOIN,\
JSON_TABLE,KEY,KEYS,KILL,LAG,LAST_VALUE,LATERAL,LEAD,LEADING,LEAVE,LEFT,\
LIMIT,LINEAR,LINES,LOAD,LOCALTIME,LOCALTIMESTAMP,LONGBLOB,LONGTEXT,\
LOW_PRIORITY,MASTER_BIND,MASTER_SSL_VERIFY_SERVER_CERT,MATCH,MAXVALUE,\
MEDIUMBLOB,MEDIUMINT,MEDIUMTEXT,MIDDLEINT,MINUTE_MICROSECOND,MINUTE_SECOND,\
MODIFIES,NO_WRITE_TO_BINLOG,NTH_VALUE,NTILE,NUMERIC,OPTIMIZE,OPTIMIZER_COSTS,\
OPTIONALLY,OUTER,OUTFILE,OVER,PERCENT_RANK,PRECISION,PRIMARY,PURGE,RANK,READ,\
READS,READ_WRITE,RECURSIVE,REFERENCES,REGEXP,REPEAT,REPLACE,REQUIRE,RESIGNAL,\
RESTRICT,RIGHT,RLIKE,ROW_NUMBER,SCHEMAS,SECOND_MICROSECOND,SENSITIVE,\
SEPARATOR,SHOW,SIGNAL,SPATIAL,SPECIFIC,SQLEXCEPTION,SQLSTATE,SQLWARNING,\
SQL_BIG_RESULT,SQL_CALC_FOUND_ROWS,SQL_SMALL_RESULT,SSL,STARTING,STORED,\
STRAIGHT_JOIN,SYSTEM,TERMINATED,TINYBLOB,TINYINT,TINYTEXT,TRAILING,UNDO,\
UNLOCK,UNSIGNED,USAGE,USING,UTC_DATE,UTC_TIME,UTC_TIMESTAMP,VARBINARY,\
VARCHARACTER,VARYING,VIRTUAL,WINDOW,WRITE,YEAR_MONTH,ZEROFILL,ABS,\
ALLOCATE,ANALYSE,ARE,ARRAY_AGG,ARRAY_MAX_CARDINALITY,ASYMMETRIC,ATOMIC,\
BEGIN_FRAME,BEGIN_PARTITION,CALLED,CARDINALITY,CASCADED,CAST,CEIL,CEILING,\
CHAR_LENGTH,CHARACTER_LENGTH,CLOB,COALESCE,COLLATION,COLLECT,CONCURRENTLY,\
CONTAINS,CORR,CORRESPONDING,COVAR_POP,COVAR_SAMP,CURRENT_CATALOG,\
CURRENT_DEFAULT_TRANSFORM_GROUP,CURRENT_PATH,CURRENT_ROLE,\
CURRENT_ROW,CURRENT_SCHEMA,CURRENT_TRANSFORM_GROUP_FOR_TYPE,CYCLE,DATALINK,\
DAY,DEALLOCATE,DEFERRABLE,DEREF,DISCONNECT,DLNEWCOPY,DLPREVIOUSCOPY,\
DLURLCOMPLETE,DLURLCOMPLETEONLY,DLURLCOMPLETEWRITE,DLURLPATH,DLURLPATHONLY,\
DLURLPATHWRITE,DLURLSCHEME,DLURLSERVER,DLVALUE,DYNAMIC,ELEMENT,END_FRAME,\
END_PARTITION,END EXEC,EQUALS,ESCAPE,EVERY,EXEC,EXECUTE,EXP,EXTERNAL,EXTRACT,\
FILTER,FLOOR,FRAME_ROW,FREE,FREEZE,FULL,FUSION,GLOBAL,HOLD,HOUR,IDENTITY,\
ILIKE,IMPORT,INITIALLY,INTERSECTION,ISNULL,LANGUAGE,LARGE,LIKE_REGEX,LN,LOCAL,\
LOWER,MAX_CARDINALITY,MEMBER,MERGE,METHOD,MINUTE,MODULE,MONTH,MULTISET,\
NATIONAL,NCHAR,NCLOB,NO,NONE,NORMALIZE,NOTNULL,NULLIF,OCCURRENCES_REGEX,\
OCTET_LENGTH,OFFSET,OLD,ONLY,OVERLAPS,OVERLAY,PARAMETER,PERCENT,\
PERCENTILE_CONT,PERCENTILE_DISC,PERIOD,PLACING,PORTION,POSITION,\
POSITION_REGEX,POWER,PRECEDES,PREPARE,REF,REFERENCING,REGR_AVGX,REGR_AVGY,\
REGR_COUNT,REGR_INTERCEPT,REGR_R2,REGR_SLOPE,REGR_SXX,REGR_SXY,REGR_SYY,\
RESULT,RETURNING,RETURNS,ROLLUP,SCOPE,SCROLL,SEARCH,SECOND,SESSION_USER,\
SIMILAR,SOME,SPECIFICTYPE,SQRT,STATIC,STDDEV_POP,STDDEV_SAMP,SUBMULTISET,\
SUBSTRING,SUBSTRING_REGEX,SUCCEEDS,SYMMETRIC,SYSTEM_TIME,SYSTEM_USER,\
TABLESAMPLE,TIME,TIMESTAMP,TIMEZONE_HOUR,TIMEZONE_MINUTE,TRANSLATE,\
TRANSLATE_REGEX,TRANSLATION,TREAT,TRIM,TRIM_ARRAY,TRUNCATE,UESCAPE,UNKNOWN,\
UNNEST,UPPER,VALUE,VALUE_OF,VAR_POP,VAR_SAMP,VARIADIC,VERBOSE,VERSIONING,\
WIDTH_BUCKET,WITHIN,WITHOUT,XML,XMLAGG,XMLATTRIBUTES,XMLBINARY,XMLCAST,\
XMLCOMMENT,XMLCONCAT,XMLDOCUMENT,XMLELEMENT,XMLEXISTS,XMLFOREST,XMLITERATE,\
XMLNAMESPACES,XMLPARSE,XMLPI,XMLQUERY,XMLSERIALIZE,XMLTABLE,XMLTEXT,\
XMLVALIDATE,YEAR,RAISERROR,FILLFACTOR,READTEXT,RECONFIGURE,FREETEXT,\
FREETEXTTABLE,BACKUP,RESTORE,BREAK,REVERT,BROWSE,BULK,HOLDLOCK,ROWCOUNT,\
ROWGUIDCOL,IDENTITY_INSERT,RULE,CHECKPOINT,IDENTITYCOL,SAVE,CLUSTERED,\
SECURITYAUDIT,SEMANTICKEYPHRASETABLE,SEMANTICSIMILARITYDETAILSTABLE,\
SEMANTICSIMILARITYTABLE,COMPUTE,SETUSER,CONTAINSTABLE,SHUTDOWN,STATISTICS,\
LINENO,TEXTSIZE,NOCHECK,NONCLUSTERED,TOP,NICHT,TRAN,TRANSACTION,DBCC,OFF,\
TRY_CONVERT,OFFSETS,TSEQUAL,DENY,OPENDATASOURCE,UNPIVOT,DISK,OPENQUERY,\
OPENROWSET,UPDATETEXT,DISTRIBUTED,OPENXML,DUMP,WAITFOR,ERRLVL,PIVOT,PLAN,\
 WITHIN,GROUP,PRINT,WRITETEXT,PROC,ABSOLUTE,ACTION,PAD,ADA,PARTIAL,PASCAL,\
FIRST,PRESERVE,FORTRAN,ASSERTION,FOUND,RELATIVE,GO,BIT,BIT_LENGTH,SECTION,\
CATALOG,INCLUDE,INPUT,location,SQLCA,SQLERROR,CONNECTION,ISOLATION,\
CONSTRAINTS,LAST,TEMPORARY,NAMES,NEXT,DEFERRED,DESCRIPTOR,DIAGNOSTICS,\
DOMAIN,OUTPUT,ZONE,HOST,ADMIN,AFTER,AGGREGATE,ROLE,ALIAS,INITIALIZE,ROUTINE,\
SEQUENCE,SETS,BREADTH,LESS,LOCATOR,CLASS,MAP,STATE,COMPLETION,STRUCTURE,\
CONSTRUCTOR,THAN,Nein,Keine,OBJECT,DATA,UNDER,OPERATION,ORDINALITY,DEPTH,\
PARAMETERS,VARIABLE,DESTROY,DESTRUCTOR,PATH,POSTFIX,DICTIONARY,PREFIX,\
PREORDER,GLEITKOMMAZAHL,KOSTENLOS,FULLTEXTTABLE,GENERAL',
            'field_options': {
                'label': 'Not allowed words',
                'help_text': 'Comma-separated list of not allowed words',
                'required': False,
                },
        },
              ]

    def checkLine(self, f, line, line_num, attributesToCheckLenght,
                  notAllowedWords, maxLength):
        # Check for too long Attribute Names
        for att in attributesToCheckLenght:
            regExString = '%s="\\w*"' % (att)
            for foundAtt in re.findall(regExString, line):
                foundAttributeName = foundAtt.split('=')[0]
                foundAttributeV = foundAtt.split('=')[1]
                foundAttributeValue = foundAttributeV.split("\"")[1]
                length = len(foundAttributeValue)
                if length > int(maxLength):
                    f.comment('Value of attribut \
                              %s is to long. Lenght is: %s. Allowed \
                              is: %s' % (foundAttributeName, length,
                              maxLength), line_num)
                # Check for blacklisted words
                for word in notAllowedWords:
                    if word.lower() == foundAttributeValue.lower():
                        f.comment('Value "%s" is blacklisted' %
                                  (word), line_num)

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        ext = splitext(f.dest_file)[1][1:]
        if not ext.lower() == "xml":  # Not a XML file
            # Ignore the file. It is not an XML file.
            return

        path = f.get_patched_file_path()
        if not path:  # Ignore the file.
            return

        notAllowedWords = settings['ReservedWords'].split(',')
        attributesToCheckLenght = settings['AttributesToCheck'].split(',')
        maxLength = settings['MaxLength']
        headerIdentifierRegex = settings['LiquibaseHeaderRegex']
        isLiquibaseFile = False

        with open(path, 'rb') as content_test:
            for line in content_test:
                if re.findall(headerIdentifierRegex, line):
                    isLiquibaseFile = True
            if not isLiquibaseFile:
                # isNotALiquibaseFile
                return
        with open(path, 'rb') as content:
            line_num = 0
            for line in content:
                line_num += 1
                self.checkLine(f, line, line_num, attributesToCheckLenght,
                               notAllowedWords, maxLength)
