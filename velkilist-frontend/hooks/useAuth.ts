import { useEffect } from 'react'
import { useUserStore } from '@/store/userStore'
import { me } from '@/services/userService'

export function useAuth() {
  const { user, setUser } = useUserStore()
  useEffect(() => {
    if (!user && typeof window !== 'undefined' && localStorage.getItem('access_token')) {
      me().then(setUser).catch(() => {})
    }
  }, [user, setUser])
  return { user }
}
