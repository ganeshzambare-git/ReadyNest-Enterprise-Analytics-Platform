import { create } from "zustand"
import { fetchFromAPI } from "@/lib/api"

interface AppState {
  workspace: string | null;
  user: any | null;
  isLoading: boolean;
  error: string | null;
  setWorkspace: (name: string) => void;
  fetchDashboardData: () => Promise<void>;
}

export const useAppStore = create<AppState>((set) => ({
  workspace: null,
  user: null,
  isLoading: false,
  error: null,
  
  setWorkspace: (name) => set({ workspace: name }),
  
  fetchDashboardData: async () => {
    set({ isLoading: true, error: null })
    try {
      // Example endpoint call to FastAPI backend
      // const data = await fetchFromAPI("/api/v1/dashboard/metrics")
      // set({ dashboardData: data, isLoading: false })
      
      // Simulating API delay for MVP
      await new Promise(resolve => setTimeout(resolve, 1000))
      set({ isLoading: false })
    } catch (error: any) {
      set({ error: error.message, isLoading: false })
    }
  }
}))
