using System;
using Xunit;

namespace Helpers.Tests
{
    public class HashCodeGeneratorTests
    {
        [Fact]
        public void HashCodeGenerator_Returns_0_For_Null()
        {
            Assert.Equal(1,0);
        }
    }
}
