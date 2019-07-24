using System;
using System.Collections.Generic;
using System.Data;

namespace Databases
{
    public class SQLQuery<T> where T : class
    {
        public string sql { get; set; }
        public string dbTable { get; set; } = null;
        public List<T> TObjects { get; set; } = null;
        public CommandType? commandType { get; set; } = null;

        public SQLQuery(string sqlquery)
        {
            sql = sqlquery;
        }

        public SQLQuery(string sqlquery, T TObjectIn, string tableName = null, CommandType? commandTypeIn = null)
        {
            sql = sqlquery;
            dbTable = tableName;
            TObjects = new List<T> { TObjectIn };
            commandType = commandTypeIn;
        }

        public SQLQuery(string sqlquery, List<T> TObjectsIn, string tableName = null, CommandType? commandTypeIn = null)
        {
            sql = sqlquery;
            dbTable = tableName;
            TObjects = TObjectsIn;
            commandType = commandTypeIn;
        }
    }

    public class SQLQuery : SQLQuery<object>
    {
        public SQLQuery(string sqlquery) : base(sqlquery)
        {

        }
    }
}
