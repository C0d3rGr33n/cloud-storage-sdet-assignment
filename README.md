# AI App Builder - Lovable.dev Clone

An AI-powered web application builder similar to Lovable.dev that generates complete, functional web applications from natural language descriptions. Built with Python, Django, FastAPI, and React.

## 🚀 Features

- **AI-Powered Code Generation**: Describe your app in plain English and watch our AI generate complete React applications
- **Modern Tech Stack**: Built with React, TypeScript, Tailwind CSS, Django, and FastAPI
- **Real-time Collaboration**: Work together with your team using WebSocket connections
- **One-Click Deployment**: Deploy your generated apps instantly
- **Smart Code Editor**: Monaco editor with AI-assisted suggestions
- **Project Management**: Full CRUD operations for projects with file versioning
- **User Authentication**: Secure JWT-based authentication system
- **Responsive Design**: All generated apps are mobile-friendly by default

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI       │    │   Django        │
│   (Port 3000)   │◄──►│   AI Service    │◄──►│   Backend       │
│                 │    │   (Port 8000)   │    │   (Port 8001)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   OpenAI API    │    │   PostgreSQL    │
                       │   Integration   │    │   Database      │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance API for AI code generation
- **Django**: Robust backend for user management and project persistence
- **PostgreSQL**: Primary database for storing users, projects, and files
- **Redis**: Caching and Celery task queue
- **Celery**: Background task processing
- **OpenAI API**: GPT-4 for code generation
- **WebSockets**: Real-time collaboration features

### Frontend
- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Monaco Editor**: VS Code-like code editor
- **Framer Motion**: Smooth animations and transitions
- **Zustand**: Lightweight state management
- **React Query**: Data fetching and caching

### Infrastructure
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and static file serving (production)

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.9 or higher)
- **Docker & Docker Compose** (recommended for development)
- **PostgreSQL** (v13 or higher)
- **Redis** (v6 or higher)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-app-builder
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - FastAPI: http://localhost:8000
   - Django Admin: http://localhost:8001/admin

### Option 2: Manual Setup

1. **Clone and setup backend**
   ```bash
   git clone <repository-url>
   cd ai-app-builder
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Setup Django
   cd django_backend
   python manage.py migrate
   python manage.py createsuperuser
   cd ..
   ```

2. **Setup frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Start services**
   ```bash
   # Terminal 1: FastAPI
   cd src
   python main.py
   
   # Terminal 2: Django
   cd django_backend
   python manage.py runserver 8001
   
   # Terminal 3: Celery
   cd django_backend
   celery -A django_backend worker -l info
   
   # Terminal 4: Frontend (if not started)
   cd frontend
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Database
DB_NAME=ai_app_builder
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
```

### API Keys Setup

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Anthropic API Key** (optional): Get from [Anthropic Console](https://console.anthropic.com/)

## 📖 API Documentation

### FastAPI Endpoints

- **POST** `/api/projects` - Create a new project from description
- **GET** `/api/projects` - List user's projects
- **GET** `/api/projects/{project_id}` - Get project details
- **POST** `/api/projects/{project_id}/edit` - Edit project code
- **POST** `/api/projects/{project_id}/chat` - Chat with AI about project
- **POST** `/api/projects/{project_id}/publish` - Deploy project
- **WebSocket** `/ws/projects/{project_id}` - Real-time collaboration

### Authentication

All protected endpoints require a Bearer token:
```bash
Authorization: Bearer <your_jwt_token>
```

## 🎨 Usage Examples

### Creating a Project

```javascript
const response = await fetch('/api/projects', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    name: 'My Recipe App',
    description: 'Create a recipe tracking app with categories and sharing features',
    tech_stack: ['react', 'tailwind', 'typescript'],
    design_preferences: 'Modern and clean design with colorful accents'
  })
});
```

### Chatting with AI

```javascript
const response = await fetch(`/api/projects/${projectId}/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    message: 'How can I add user authentication to this app?',
    project_id: projectId
  })
});
```

## 🧪 Testing

### Backend Tests
```bash
# FastAPI tests
cd src
python -m pytest tests/

# Django tests
cd django_backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Docker Setup

1. **Create production environment file**
   ```bash
   cp .env.example .env.production
   # Update with production values
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Manual Production Deployment

1. **Build frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /path/to/frontend/build;
           try_files $uri $uri/ /index.html;
       }
       
       location /api/ {
           proxy_pass http://localhost:8000;
       }
   }
   ```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Lovable.dev](https://lovable.dev)
- Built with [OpenAI GPT-4](https://openai.com)
- UI components from [Tailwind UI](https://tailwindui.com)
- Icons from [Heroicons](https://heroicons.com)

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs on [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/your-repo/discussions)

## 🗺️ Roadmap

- [ ] **Phase 1**: Core AI generation (✅ Completed)
- [ ] **Phase 2**: Real-time collaboration
- [ ] **Phase 3**: Advanced deployment options
- [ ] **Phase 4**: Template marketplace
- [ ] **Phase 5**: Plugin system
- [ ] **Phase 6**: Mobile app builder

---

**Built with ❤️ and AI** | [Demo](https://your-demo-url.com) | [Documentation](https://your-docs-url.com)
