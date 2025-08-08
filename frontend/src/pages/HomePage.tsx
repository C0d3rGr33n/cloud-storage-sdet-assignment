import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  CodeBracketIcon, 
  RocketLaunchIcon,
  CpuChipIcon,
  GlobeAltIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      {/* Navigation */}
      <nav className="relative px-4 py-6 flex justify-between items-center bg-white/80 backdrop-blur-sm border-b border-gray-100">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <SparklesIcon className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI App Builder
          </span>
        </div>
        
        <div className="flex items-center space-x-4">
          <Link
            to="/explore"
            className="text-gray-600 hover:text-gray-900 transition-colors"
          >
            Explore
          </Link>
          <Link
            to="/login"
            className="text-gray-600 hover:text-gray-900 transition-colors"
          >
            Sign In
          </Link>
          <Link
            to="/register"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-4 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Build Apps with{' '}
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Magic
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Describe your app idea in plain English and watch our AI generate a complete, 
            functional web application in minutes. No coding required.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              Start Building for Free
            </Link>
            <Link
              to="/explore"
              className="border border-gray-300 hover:border-gray-400 text-gray-700 px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              View Examples
            </Link>
          </div>
        </motion.div>

        {/* Demo Video/Screenshot Placeholder */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="mt-16 max-w-4xl mx-auto"
        >
          <div className="bg-white rounded-2xl shadow-2xl p-2">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl h-96 flex items-center justify-center">
              <div className="text-white text-center">
                <CodeBracketIcon className="w-16 h-16 mx-auto mb-4" />
                <p className="text-xl font-semibold">Interactive Demo Coming Soon</p>
                <p className="text-blue-100 mt-2">Watch AI generate a complete app in real-time</p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Everything you need to build amazing apps
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform handles the entire development process, 
              from design to deployment.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: SparklesIcon,
                title: 'AI-Powered Generation',
                description: 'Describe your app in natural language and watch our AI create it instantly.',
                color: 'from-yellow-400 to-orange-500'
              },
              {
                icon: CodeBracketIcon,
                title: 'Modern Tech Stack',
                description: 'Built with React, TypeScript, Tailwind CSS, and other cutting-edge technologies.',
                color: 'from-blue-400 to-blue-600'
              },
              {
                icon: RocketLaunchIcon,
                title: 'One-Click Deployment',
                description: 'Deploy your app instantly with our integrated hosting platform.',
                color: 'from-purple-400 to-purple-600'
              },
              {
                icon: CpuChipIcon,
                title: 'Smart Code Editor',
                description: 'Edit and customize your generated code with AI-assisted suggestions.',
                color: 'from-green-400 to-green-600'
              },
              {
                icon: GlobeAltIcon,
                title: 'Responsive Design',
                description: 'Every app is automatically optimized for desktop, tablet, and mobile.',
                color: 'from-indigo-400 to-indigo-600'
              },
              {
                icon: UserGroupIcon,
                title: 'Real-time Collaboration',
                description: 'Work together with your team in real-time with live editing and chat.',
                color: 'from-pink-400 to-pink-600'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-gray-50 rounded-xl p-6 hover:shadow-lg transition-shadow"
              >
                <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center mb-4`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="px-4 py-20 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How it works
            </h2>
            <p className="text-xl text-gray-600">
              From idea to deployed app in just three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Describe Your App',
                description: 'Tell us what you want to build in plain English. Be as detailed or as simple as you like.',
                example: '"Create a recipe tracking app with categories and sharing features"'
              },
              {
                step: '02',
                title: 'AI Generates Code',
                description: 'Our AI analyzes your description and generates a complete, functional application.',
                example: 'Complete React app with components, styling, and functionality'
              },
              {
                step: '03',
                title: 'Deploy & Share',
                description: 'Review, customize, and deploy your app with a single click. Share it with the world!',
                example: 'Live app accessible via custom URL'
              }
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="relative"
              >
                <div className="bg-white rounded-xl p-6 shadow-sm">
                  <div className="text-4xl font-bold text-blue-600 mb-4">
                    {step.step}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 mb-4">
                    {step.description}
                  </p>
                  <div className="bg-gray-50 rounded-lg p-3 text-sm text-gray-700 font-mono">
                    {step.example}
                  </div>
                </div>
                
                {index < 2 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center transform -translate-y-1/2">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 py-20 bg-gray-900">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to build your next app?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of developers who are already building with AI
          </p>
          <Link
            to="/register"
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors inline-block"
          >
            Get Started for Free
          </Link>
          <p className="text-gray-400 mt-4 text-sm">
            No credit card required • Free forever plan available
          </p>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-50 px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <SparklesIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI App Builder
              </span>
            </div>
            
            <div className="flex space-x-6 text-gray-600">
              <Link to="/explore" className="hover:text-gray-900 transition-colors">
                Explore
              </Link>
              <a href="#" className="hover:text-gray-900 transition-colors">
                Documentation
              </a>
              <a href="#" className="hover:text-gray-900 transition-colors">
                Support
              </a>
              <a href="#" className="hover:text-gray-900 transition-colors">
                Privacy
              </a>
            </div>
          </div>
          
          <div className="border-t border-gray-200 mt-8 pt-8 text-center text-gray-600">
            <p>&copy; 2024 AI App Builder. Built with ❤️ and AI.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;