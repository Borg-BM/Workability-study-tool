// The signed-in user, as App.tsx gets it from getMe() (api.ts) after the Authentik SSO
// sign-in -- the backend identifies every request by its session cookie, not by anything
// the frontend sends. Every ownership/permission check keys off `email`.
export interface Identity {
  email: string
  name: string
}
