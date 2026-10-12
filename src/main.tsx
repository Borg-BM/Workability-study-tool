// Standard Vite/React entrypoint -- mounts <App/> into index.html's #root div.
// StrictMode double-invokes effects/renders in dev to surface side-effect bugs early;
// it has no effect on the production build.
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
