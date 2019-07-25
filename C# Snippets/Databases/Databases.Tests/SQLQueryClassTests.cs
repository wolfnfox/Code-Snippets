using System;
using System.Collections.Generic;
using Xunit;

namespace Databases.Tests
{
    public class SQLQueryClassTests
    {
        [Fact]
        public void Initialise_SQLQuery_Class_With_No_Parameters()
        {
            SQLQuery sqlQuery = new SQLQuery(null);
            Assert.Null(sqlQuery.sql);
            Assert.Null(sqlQuery.TObjects);
            Assert.Null(sqlQuery.commandType);
        }
    }
}
