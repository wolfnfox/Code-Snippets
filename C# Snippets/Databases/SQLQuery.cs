using System;
using System.Collections.Generic;
using System.Data;

using Helpers;

namespace Databases
{
    /// <summary>
    /// Class for holding the SQL query <see cref="string"/> containing parameters and the query <see cref="object"/>(s).
    /// </summary>
    /// <typeparam name="T">The type of the entity.</typeparam>
    public class SQLQuery<T> : IEquatable<SQLQuery<T>> where T : class
    {
        public string sql { get; set; }
        public List<T> TObjects { get; set; } = null;
        public CommandType? commandType { get; set; } = null;
        public string dbTableName { get; set; } = null;         // NOT CURRENTLY USED by CommonDbAccess class
        public bool isBulk { get; set; } = false;               // NOT CURRENTLY USED by CommonDbAccess class
        public int batchSize { get; set; } = 0;                 // NOT CURRENTLY USED by CommonDbAccess class

        /// <summary>
        /// <para>Initializes a new instance of <see cref="SQLQuery"/>.</para>
        /// <para>Use this when the query <see cref="string"/> contains no parameters. <br />
        /// Use <see cref="CommandType.StoredProcedure"/> if the query <see cref="string"/> is a stored procedure.</para>
        /// </summary>
        /// <param name="sqlquery">The SQL query <see cref="string"/>.</param>
        /// <param name="commandType">Specify the <see cref="CommandType"/>.<br />(e.g <see cref="CommandType.StoredProcedure"/>)</param>
        /// <exception cref="System.ArgumentNullException"> if SQL <see cref="string"/> is <see cref="null"/>.</exception>
        public SQLQuery(string sqlquery, CommandType? commandType = null)
        {
            sql = sqlquery ?? throw new ArgumentNullException(nameof(sqlquery));
            this.commandType = commandType;
        }

        /// <summary>
        /// <para>Initializes a new instance of <see cref="SQLQuery"/>.</para>
        ///<para>Use this when the query <see cref="string"/> contains parameters.<br />
        /// Parameters are passed in as a class <see cref="object"/> of <see cref="Type"/> T as an input parameter.<br />
        /// Use <see cref="CommandType.StoredProcedure"/> if the query <see cref="string"/> is a stored procedure.</para>
        /// </summary>
        /// <typeparam name="T">The type of the entity.</typeparam>
        /// <param name="sqlquery"></param>
        /// <param name="TObject"></param>
        /// <param name="commandType"></param>
        /// <param name="dbTableName"></param>
        /// <param name="isBulk"></param>
        /// <param name="batchSize"></param>
        /// <exception cref="System.ArgumentNullException"> if SQL <see cref="string"/> is <see cref="null"/>.</exception>
        /// <exception cref="System.ArgumentNullException"> if passed in <see cref="object"/> is <see cref="null"/>.</exception>
        public SQLQuery(string sqlquery, T TObject, CommandType? commandType = null, string dbTableName = null, bool isBulk = false, int batchSize = 0)
        {
            if (TObject == null) throw new ArgumentNullException(nameof(TObject));
            sql = sqlquery ?? throw new ArgumentNullException(nameof(sqlquery));
            TObjects = new List<T> { TObject };
            this.commandType = commandType;
            this.dbTableName = dbTableName;
            this.isBulk = isBulk;
            this.batchSize = batchSize;
        }

        /// <summary>
        /// <para>Initializes a new instance of <see cref="SQLQuery"/>.</para>
        ///<para>Use this when the query <see cref="string"/> contains parameters.<br />
        /// Parameters are passed in as a class <see cref="object"/> of <see cref="Type"/> T as an input parameter.<br />
        /// Use <see cref="CommandType.StoredProcedure"/> if the query <see cref="string"/> is a stored procedure.</para>
        /// </summary>
        /// <param name="sqlquery"></param>
        /// <param name="TObjects"></param>
        /// <param name="commandType"></param>
        /// <param name="dbTableName"></param>
        /// <param name="isBulk"></param>
        /// <param name="batchSize"></param>
        /// <exception cref="System.ArgumentNullException"> if SQL <see cref="string"/> is <see cref="null"/>.</exception>
        /// <exception cref="System.ArgumentNullException"> if passed in <see cref="object"/> is <see cref="null"/>.</exception>
        public SQLQuery(string sqlquery, List<T> TObjects, CommandType? commandType = null, string dbTableName = null, bool isBulk = false, int batchSize = 0)
        {
            sql = sqlquery ?? throw new ArgumentNullException(nameof(sqlquery));
            this.TObjects = TObjects ?? throw new ArgumentNullException(nameof(TObjects));
            this.commandType = commandType;
            this.dbTableName = dbTableName;
            this.isBulk = isBulk;
            this.batchSize = batchSize;
        }

        /// <summary>
        /// <para>Implementation of <see cref="IEquatable{T}"/> for <see cref="SQLQuery"/>.</para>
        /// <para>Returns true if <see cref="SQLQuery"/> references the same <see cref="object"/> or its members are equal.</para>
        /// </summary>
        /// <param name="other"></param>
        /// <returns></returns>
        public bool Equals(SQLQuery<T> other)
        {
            if (ReferenceEquals(other, null))
                return false;

            if (ReferenceEquals(this, other))
                return true;

            return (sql.Equals(other.sql) 
        &&  dbTableName.Equals(other.dbTableName)
        &&     TObjects.Equals(other.TObjects)
        &&  commandType.Equals(other.commandType)
        &&       isBulk.Equals(other.isBulk)
        &&    batchSize.Equals(other.batchSize));
        }

        /// <summary>
        /// Override of <see cref="object.Equals(object)"/> method for <see cref="SQLQuery"/>.
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public override bool Equals(Object obj)
        {
            if (obj == null)
                return false;

            SQLQuery<T> sqlQueryObj = obj as SQLQuery<T>;
            if (sqlQueryObj == null)
                return false;
            else
                return Equals(sqlQueryObj);
        }

        /// <summary>
        /// Override of <see cref="object.GetHashCode"/> method for <see cref="SQLQuery"/>.
        /// </summary>
        /// <returns><see cref="int"/> HashCode</returns>
        public override int GetHashCode()
        {
            return HashCodeGenerator.StartHash().Hash(sql).Hash(dbTableName).Hash(TObjects).Hash(commandType).Hash(isBulk).Hash(batchSize);
        }

        /// <summary>
        /// Override of equality operator for <see cref="SQLQuery"/>.
        /// </summary>
        /// <param name="sqlQuery1"></param>
        /// <param name="sqlQuery2"></param>
        /// <returns></returns>
        public static bool operator == (SQLQuery<T> sqlQuery1, SQLQuery<T> sqlQuery2)
        {
            if (((object)sqlQuery1) == null || ((object)sqlQuery2) == null)
                return Object.Equals(sqlQuery1, sqlQuery2);

            return sqlQuery1.Equals(sqlQuery2);
        }

        /// <summary>
        /// Override of inequality operator for <see cref="SQLQuery"/>
        /// </summary>
        /// <param name="sqlQuery1"></param>
        /// <param name="sqlQuery2"></param>
        /// <returns></returns>
        public static bool operator != (SQLQuery<T> sqlQuery1, SQLQuery<T> sqlQuery2)
        {
            if (((object)sqlQuery1) == null || ((object)sqlQuery2) == null)
                return !Object.Equals(sqlQuery1, sqlQuery2);

            return !(sqlQuery1.Equals(sqlQuery2));
        }
    }

    /// <summary>
    /// Class for holding the SQL query <see cref="string"/>.
    /// </summary>
    public class SQLQuery : SQLQuery<object>
    {
        /// <summary>
        /// <para>Initializes a new instance of <see cref="SQLQuery"/>.</para>
        /// <para>Use this when the query <see cref="string"/> contains no parameters. <br />
        /// Use <see cref="CommandType.StoredProcedure"/> if the query <see cref="string"/> is a stored procedure.</para>
        /// </summary>
        /// <param name="sqlquery">The SQL query <see cref="string"/>.</param>
        /// <param name="commandType">Specify the <see cref="CommandType"/>.<br />(e.g <see cref="CommandType.StoredProcedure"/>)</param>
        /// <exception cref="System.ArgumentNullException"> if SQL <see cref="string"/> is <see cref="null"/>.</exception>
        public SQLQuery(string sqlquery, CommandType? commandType = null) : base(sqlquery, commandType)
        {
            if (sqlquery == null) throw new ArgumentNullException(nameof(sqlquery));
        }
    }
}
