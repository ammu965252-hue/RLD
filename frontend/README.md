# Rice Leaf Detection - Frontend

A modern, responsive web interface for the Rice Leaf Disease Detection system. This frontend provides users with an intuitive platform to upload leaf images, view detection results, access detection history, and interact with an AI chatbot for farming advice.

## 📁 Project Structure

```
frontend/
├── index.html                 # Home / Upload page
├── result.html                # Detection result page
├── history.html               # Detection history
├── chatbot.html               # AI farmer chatbot
├── dashboard.html             # Dashboard & analytics
├── about.html                 # About project
├── login.html                 # Login page
├── register.html              # Register page
│
├── css/
│   ├── variables.css          # Color system & fonts (CSS variables)
│   ├── base.css               # Reset, typography, layout helpers
│   ├── components.css         # Navbar, cards, buttons, tables
│   ├── pages.css              # Page-specific styles
│   └── animations.css         # Fade, slide, pulse animations
│
├── js/
│   ├── main.js                # Global JS (navbar, theme, utils)
│   ├── upload.js              # Image upload & preview logic
│   ├── result.js              # Result page logic
│   ├── history.js             # Search, filter, table logic
│   ├── chatbot.js             # Chatbot message logic
│   ├── auth.js                # Login & register logic
│   └── dashboard.js           # Charts & stats logic
│
├── assets/
│   ├── images/
│   │   ├── hero-bg.png
│   │   ├── logo.png
│   │   └── placeholders/
│   └── icons/
│
└── README.md                  # Project documentation

```

## 🎨 Design System

### Color Palette
- **Primary**: #2ecc71 (Green) - Main actions and highlights
- **Secondary**: #3498db (Blue) - Secondary actions
- **Danger**: #e74c3c (Red) - Destructive actions
- **Warning**: #f39c12 (Orange) - Warnings and alerts
- **Neutrals**: Gray scale from dark to light

### Typography
- **Primary Font**: Segoe UI, Tahoma, Geneva, Verdana
- **Secondary Font**: Georgia (serif)
- **Monospace**: Courier New

### Spacing & Layout
- Uses CSS custom properties for consistent spacing
- Responsive grid layout with flexbox
- Mobile-first design approach

## 🛠️ Technologies

- **HTML5** - Semantic markup
- **CSS3** - Custom properties, Grid, Flexbox, Animations
- **Vanilla JavaScript** - No dependencies for core functionality
- **Chart.js** (optional) - For dashboard analytics
- **LocalStorage API** - Client-side data persistence

## 🚀 Features

### Pages

#### 1. **Home / Upload (index.html)**
- Drag-and-drop image upload
- Click to browse file selection
- Image preview before upload
- File validation (type and size)

#### 2. **Detection Results (result.html)**
- Display detected disease name
- Show confidence score
- Display severity level
- Provide recommendations
- Download report option

#### 3. **History (history.html)**
- View all past detection results
- Search by disease name or ID
- Filter by severity level
- Filter by date range
- Sortable table
- Delete old results

#### 4. **AI Farmer Chatbot (chatbot.html)**
- Real-time chat interface
- Typing indicators
- Message history
- Agricultural advice integration

#### 5. **Dashboard (dashboard.html)**
- Key statistics cards
- Scan trends visualization
- Disease distribution charts
- Download reports
- Export data (CSV/JSON)

#### 6. **Authentication (login.html, register.html)**
- User registration
- Secure login
- Form validation
- Error handling

#### 7. **About (about.html)**
- Project information
- Team member profiles
- Project goals and technology stack

## 🎭 CSS Modules

### variables.css
Defines the design system through CSS custom properties:
- Colors and gradients
- Typography scales
- Spacing system
- Border radius tokens
- Shadow definitions
- Transition durations

### base.css
Foundation styles:
- CSS reset
- Typography hierarchy
- Layout utilities
- Display helpers
- Spacing utilities

### components.css
Reusable UI components:
- Navbar styling
- Card components
- Button variants (primary, secondary, danger, outline)
- Form elements
- Tables
- Badges and alerts

### pages.css
Page-specific styling:
- Upload interface styles
- Result display layouts
- History table styling
- Chatbot message interface
- Dashboard grid
- Authentication page styling

### animations.css
Animation library:
- Fade in/out
- Slide animations (left, right, up, down)
- Pulse effects
- Scale animations
- Spin and bounce
- Custom animations

## 📜 JavaScript Modules

### main.js
Global utilities and functions:
- Theme toggle (light/dark mode)
- Navbar interaction
- Notification system
- API wrapper function
- LocalStorage helpers
- Date/file formatting

### upload.js
Image upload functionality:
- Drag-and-drop handling
- File validation
- Image preview
- Server upload with progress

### result.js
Result display logic:
- Load result data from API
- Display formatted results
- Download report functionality

### history.js
Detection history management:
- Load history from API
- Filter and search functionality
- Delete results
- Date range filtering

### chatbot.js
Chatbot interface logic:
- Send messages
- Display chat bubbles
- Typing indicators
- Chat history loading

### auth.js
Authentication logic:
- Login form handling
- Registration form handling
- Token management
- Protected route checking

### dashboard.js
Analytics and dashboard:
- Load statistics
- Chart rendering (Chart.js)
- Data export
- Report generation

## 🔌 API Integration Points

The frontend expects the following API endpoints:

```javascript
// Upload
POST /api/upload

// Results
GET /api/result/:id
DELETE /api/result/:id
GET /api/result/:id/download

// History
GET /api/history

// Chatbot
POST /api/chatbot/message
GET /api/chatbot/history

// Dashboard
GET /api/dashboard/stats
GET /api/dashboard/report
GET /api/dashboard/export?format=csv

// Authentication
POST /api/auth/login
POST /api/auth/register
```

## 🎯 Usage

### Local Development
1. Open any HTML file in a browser
2. No build process needed
3. LocalStorage used for theme and session data

### Production Deployment
1. Minify CSS and JavaScript
2. Optimize images
3. Set up CORS if backend is on different domain
4. Configure API base URL
5. Add security headers

## 🎨 Customization

### Changing Colors
Edit `css/variables.css`:
```css
:root {
    --primary: #2ecc71;        /* Change primary color */
    --secondary: #3498db;      /* Change secondary color */
}
```

### Adding Animations
Add new keyframes in `css/animations.css` and apply to elements:
```html
<div class="fade-in">Animated content</div>
```

### Creating New Pages
1. Create new HTML file
2. Include CSS files
3. Include `main.js`
4. Include page-specific JS
5. Update navbar navigation

## ⚡ Performance Optimization

- CSS organized in separate files for better caching
- Minimal JavaScript dependencies
- LocalStorage for client-side data
- Lazy loading ready
- Mobile-optimized layout

## 🔒 Security Considerations

- Sanitize user inputs
- Validate file uploads on backend
- Use HTTPS for API calls
- Store auth tokens securely
- Implement CORS properly
- Add CSP headers

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

When adding new features:
1. Keep CSS modular
2. Use CSS variables for colors and spacing
3. Follow existing naming conventions
4. Add comments for complex logic
5. Test on mobile devices

## 📝 License

[Add your license information here]

## 📧 Contact

[Add contact information here]
