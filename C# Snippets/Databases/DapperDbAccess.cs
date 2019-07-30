using Dapper;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Text;
using System.Threading.Tasks;

namespace Databases
{
    public class DapperDbAccess
    {
        private readonly IConfiguration _configuration;
        private readonly string _connectionString;

        public DapperDbAccess(IConfiguration configuration, string key)
        {
            _configuration = configuration;
            _connectionString = _configuration[key];
        }

        protected List<T> Select<T>(SQLQuery<T> sqlQuery) where T : class
        {
            return Query(sqlQuery);
        }

        protected int Delete<T>(SQLQuery<T> sqlQuery) where T : class
        {
            return Execute(sqlQuery);
        }

        protected int Insert<T>(SQLQuery<T> sqlQuery) where T : class
        {
            return Execute(sqlQuery);
        }

        protected int Update<T>(SQLQuery<T> sqlQuery) where T : class
        {
            return Execute(sqlQuery);
        }

        protected int Execute<T>(SQLQuery<T> sqlQuery) where T : class
        {
            return Execute(new List<SQLQuery<T>> { sqlQuery })[0];
        }

        protected List<int> Execute<T>(List<SQLQuery<T>> sqlQuerys) where T : class
        {
            using (var dbconnection = new SqlConnection(_connectionString))
            {
                dbconnection.Open();
                var transaction = dbconnection.BeginTransaction();
                try
                {
                    var result = new List<int>();
                    foreach (var sqlQuery in sqlQuerys)
                    {
                        var response = dbconnection.Execute(sqlQuery.SQL, sqlQuery.TObjects, transaction: transaction, commandType: sqlQuery.CommandType);
                        result.Add(response);
                    }
                    transaction.Commit();
                    dbconnection.Close();
                    return result;
                }
                catch
                {
                    transaction.Rollback();
                    throw;
                }
            }
        }

        protected List<T> Query<T>(SQLQuery<T> sqlQuery) where T : class
        {
            using (var dbconnection = new SqlConnection(_connectionString))
            {
                var result = new List<T>();
                if (sqlQuery.TObjects == null)
                {
                    var response = dbconnection.Query<T>(sqlQuery.SQL, commandType: sqlQuery.CommandType);
                    result.AddRange(response);
                }
                else
                {
                    foreach (var TObject in sqlQuery.TObjects)
                    {
                        var response = dbconnection.Query<T>(sqlQuery.SQL, TObject, commandType: sqlQuery.CommandType);
                        result.AddRange(response);
                    }
                }
                return result;
            }
        }

        protected async Task<int> ExecuteAsync<T>(SQLQuery<T> sqlQuery) where T : class
        {
            var response = await ExecuteAsync(new List<SQLQuery<T>> { sqlQuery });
            return response[0];
        }

        protected async Task<List<int>> ExecuteAsync<T>(List<SQLQuery<T>> sqlQuerys) where T : class
        {
            using (var dbconnection = new SqlConnection(_connectionString))
            {
                await dbconnection.OpenAsync();
                var transaction = dbconnection.BeginTransaction();
                try
                {
                    var result = new List<int>();
                    foreach (var sqlQuery in sqlQuerys)
                    {
                        var response = await dbconnection.ExecuteAsync(sqlQuery.SQL, sqlQuery.TObjects, transaction: transaction, commandType: sqlQuery.CommandType);
                        result.Add(response);
                    }
                    transaction.Commit();
                    dbconnection.Close();
                    return result;
                }
                catch
                {
                    transaction.Rollback();
                    throw;
                }
            }
        }

        protected async Task<List<T>> QueryAsync<T>(SQLQuery<T> sqlQuery) where T : class
        {
            using (var dbconnection = new SqlConnection(_connectionString))
            {
                var result = new List<T>();
                if (sqlQuery.TObjects == null)
                {
                    var response = await dbconnection.QueryAsync<T>(sqlQuery.SQL, commandType: sqlQuery.CommandType);
                    result.AddRange(response);
                }
                else
                {
                    foreach (var TObject in sqlQuery.TObjects)
                    {
                        var response = await dbconnection.QueryAsync<T>(sqlQuery.SQL, TObject, commandType: sqlQuery.CommandType);
                        result.AddRange(response);
                    }
                }
                return result;
            }
        }
    }
}
