import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('CareBridge interface error', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="error-page" role="alert">
          <div className="panel">
            <span className="eyebrow">Interface error</span>
            <h1>This page could not be displayed</h1>
            <p>Your data has not been changed. Reload the application and try again.</p>
            <button className="button primary" onClick={() => window.location.reload()}>
              Reload application
            </button>
          </div>
        </main>
      )
    }

    return this.props.children
  }
}
