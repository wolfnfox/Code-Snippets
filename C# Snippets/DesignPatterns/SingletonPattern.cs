using System;

namespace DesignPatterns
{
    public class SingletonPattern
    {
        public static SingletonPattern Instance => _instance.Value;
        public static bool InstanceExists => _instance.IsValueCreated;
        private static Lazy<SingletonPattern> _instance = new Lazy<SingletonPattern>(() => new SingletonPattern());

        private SingletonPattern()
        {

        }
    }
}
