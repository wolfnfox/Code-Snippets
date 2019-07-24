﻿using Dapper;
using Dapper.FluentMap;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;

using Databases.Models;
using System.Data.SqlClient;
using System.Linq;

namespace Databases
{
    public class CRUDExamples
    {
        public class UsingDapper
        {
            private readonly IConfiguration _configuration;
            private readonly string _connectionString;

            public UsingDapper(IConfiguration configuration, string key)
            {
                _configuration = configuration;
                _connectionString = _configuration[key];
                FluentMapper.Initialize(config => {
                    config.AddMap(new ExampleDBModel.ExampleDBModelMap());
                });
            }

            public List<ExampleDBModel> SelectAll()
            {
                string sql = @"SELECT * FROM [dbo].[ExampleDBModel]";
                using (var dbconnection = new SqlConnection(_connectionString))
                {
                    dbconnection.Open();
                    var response = dbconnection.Query<ExampleDBModel>(sql);
                    return response.ToList();
                }
            }

            public int Insert(ExampleDBModel exampleDBModel)
            {
                string sql = @"INSERT INTO [dbo].[ExampleDBModel]
                                ([Name],[DoB],[Office Location],[Currently Employed],[Salary]
                               VALUES (@Name, @DoB @OfficeLocation, @CurrentlyEmployed, @Salary)";
                using (var dbconnection = new SqlConnection(_connectionString))
                {
                    dbconnection.Open();
                    var transaction = dbconnection.BeginTransaction();
                    try
                    {
                        var response = dbconnection.Execute(sql, exampleDBModel);
                        transaction.Commit();
                        return response;
                    }
                    catch
                    {
                        transaction.Rollback();
                        throw;
                    }
                }
            }

            public int Insert(List<ExampleDBModel> exampleDBModel)
            {
                string sql = @"INSERT INTO [dbo].[ExampleDBModel]
                                ([Name],[DoB],[Office Location],[Currently Employed],[Salary]
                               VALUES (@Name, @DoB @OfficeLocation, @CurrentlyEmployed, @Salary)";
                using (var dbconnection = new SqlConnection(_connectionString))
                {
                    dbconnection.Open();
                    var transaction = dbconnection.BeginTransaction();
                    try
                    {
                        var response = dbconnection.Execute(sql, exampleDBModel);
                        transaction.Commit();
                        return response;
                    }
                    catch
                    {
                        transaction.Rollback();
                        throw;
                    }
                }
            }

            public int Delete(ExampleDBModel exampleDBModel)
            {
                string sql = @"DELETE FROM [dbo].[ExampleDBModel]
                                WHERE [Currently Employed] = @CurrentlyEmployed";
                return ExecuteSql(sql, exampleDBModel);
            }

            public int Update(List<ExampleDBModel> exampleDBModel)
            {
                string sql = @"UPDATE INTO [dbo].[ExampleDBModel]
                                WHERE [ID] = @ID";
                return ExecuteSql(sql, exampleDBModel);
            }

            private int ExecuteSql(string sql, ExampleDBModel exampleDBModel)
            {
                using (var dbconnection = new SqlConnection(_connectionString))
                {
                    dbconnection.Open();
                    var transaction = dbconnection.BeginTransaction();
                    try
                    {
                        var response = dbconnection.Execute(sql, exampleDBModel);
                        transaction.Commit();
                        return response;
                    }
                    catch
                    {
                        transaction.Rollback();
                        throw;
                    }
                }
            }

            private int ExecuteSql(string sql, List<ExampleDBModel> exampleDBModel)
            {
                using (var dbconnection = new SqlConnection(_connectionString))
                {
                    dbconnection.Open();
                    var transaction = dbconnection.BeginTransaction();
                    try
                    {
                        var response = dbconnection.Execute(sql, exampleDBModel);
                        transaction.Commit();
                        return response;
                    }
                    catch
                    {
                        transaction.Rollback();
                        throw;
                    }
                }
            }
        }

        public class UsingCommonDbAccess : CommonDbAccess
        {
            private static string _deleteQuery = @"DELETE FROM [dbo].[ExampleDBModel]
                                                    WHERE [Currently Employed] = @CurrentlyEmployed";
            private static string _insertQuery = @"INSERT INTO [dbo].[ExampleDBModel]
                                                          ([Name],[DoB],[Office Location],[Currently Employed],[Salary])
                                                   VALUES (@Name, @DoB @OfficeLocation, @CurrentlyEmployed, @Salary)";
            private static string _selectQuery = @"SELECT * FROM [dbo].[ExampleDBModel]";
            private static string _updateQuery = @"UPDATE INTO [dbo].[ExampleDBModel]
                                                    WHERE [ID] = @ID";

            public UsingCommonDbAccess(IConfiguration configuration, string key) : base(configuration, key)
            {
                FluentMapper.Initialize(config => {
                    config.AddMap(new ExampleDBModel.ExampleDBModelMap());
                });
            }

            public List<ExampleDBModel> SelectAllRecords()
            {
                return base.Select(new SQLQuery<ExampleDBModel>(_selectQuery));
            }

            public int Insert(ExampleDBModel exampleDBModel)
            {
                return base.Insert(new SQLQuery<ExampleDBModel>(_insertQuery, exampleDBModel));
            }

            public int Insert(List<ExampleDBModel> exampleDBModels)
            {
                return base.Insert(new SQLQuery<ExampleDBModel>(_insertQuery, exampleDBModels));
            }

            public int Delete(ExampleDBModel exampleDBModel)
            {
                return base.Delete(new SQLQuery<ExampleDBModel>(_deleteQuery, exampleDBModel));
            }

            public int Delete(List<ExampleDBModel> exampleDBModels)
            {
                return base.Delete(new SQLQuery<ExampleDBModel>(_deleteQuery, exampleDBModels));
            }

            public int Update(ExampleDBModel exampleDBModel)
            {
                return base.Update(new SQLQuery<ExampleDBModel>(_updateQuery, exampleDBModel));
            }

            public int Update(List<ExampleDBModel> exampleDBModels)
            {
                return base.Update(new SQLQuery<ExampleDBModel>(_updateQuery, exampleDBModels));
            }

            public List<int> DeleteAndInsert(List<ExampleDBModel> deleteRows, List<ExampleDBModel> insertRows)
            {
                List<SQLQuery<ExampleDBModel>> sqlQueries = new List<SQLQuery<ExampleDBModel>>();
                sqlQueries.Add(new SQLQuery<ExampleDBModel>(_deleteQuery, deleteRows));
                sqlQueries.Add(new SQLQuery<ExampleDBModel>(_insertQuery, insertRows));
                return base.Execute(sqlQueries);
            }
        }
    }
}