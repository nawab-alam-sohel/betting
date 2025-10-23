import axiosInstance from './axiosInstance'

// Backwards-compatible default export for API calls via axios
export default axiosInstance

// Optional helpers for convenience
export const get = async <T = any>(url: string, config?: any): Promise<T> => {
	const res = await axiosInstance.get<T>(url, config)
	return res.data as T
}
export const post = async <T = any>(url: string, data?: any, config?: any): Promise<T> => {
	const res = await axiosInstance.post<T>(url, data, config)
	return res.data as T
}

