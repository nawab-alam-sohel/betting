import { create } from 'zustand'

type User = { id: number; email: string; name?: string } | null

type State = {
  user: User
  setUser: (u: User) => void
  logout: () => void
}

export const useUserStore = create<State>((set) => ({
  user: null,
  setUser: (u) => set({ user: u }),
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
    set({ user: null })
  },
}))
