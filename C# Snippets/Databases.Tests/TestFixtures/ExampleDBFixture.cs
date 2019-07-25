using CsvHelper;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Databases.Models;

namespace Databases.Tests.TestFixtures
{
    public class ExampleDBFixture : IDisposable
    {
        public CRUDExamples.UsingDapper usingDapper;
        public CRUDExamples.UsingCommonDbAccess usingCommonDbAccess;
        public List<ExampleDBModel> exampleTestData;

        private readonly IConfiguration _configuration;
        private readonly string _connectionString;

        public ExampleDBFixture()
        {
            _configuration = new ConfigurationBuilder()
                                    .SetBasePath(Directory.GetCurrentDirectory() + @"..\..\..\..\")
                                    .AddJsonFile("dbsettings.json").Build();
            _connectionString = _configuration["AppSettings:ConnString"];
            usingDapper = new CRUDExamples.UsingDapper(_configuration, "AppSettings:ConnString");
            usingCommonDbAccess = new CRUDExamples.UsingCommonDbAccess(_configuration, "AppSettings:ConnString");
        }

        public void Dispose()
        {

        }
    }
}
