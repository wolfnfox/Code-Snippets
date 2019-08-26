using Xunit;

[assembly: CollectionBehavior(CollectionBehavior.CollectionPerClass, DisableTestParallelization = true)]
namespace DesignPatterns.Tests
{
    public class TestsSingletonPattern
    {
        public class Functionality
        {

        }

        public class UnitTests
        {
            [Fact]
            void SingletonPattern_Returns_False_If_Instance_Doesnt_Exist()
            {
                Assert.False(SingletonPattern.InstanceExists);
            }

            [Fact]
            void SingletonPattern_Returns_True_If_Instance_Initialised()
            {
                Assert.False(SingletonPattern.InstanceExists);
                var pattern = SingletonPattern.Instance;
                Assert.True(SingletonPattern.InstanceExists);
            }

            [Fact]
            void SingletonPattern_Returns_Same_Instance_For_Each_Call()
            {
                var pattern1 = SingletonPattern.Instance;
                var pattern2 = SingletonPattern.Instance;
                Assert.Equal(pattern1, pattern2);
            }
        }
    }
}
