import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { LandingPage } from '@/pages/LandingPage'
import { CaseBoardPage } from '@/pages/CaseBoardPage'
import { QuestStoryPage } from '@/pages/QuestStoryPage'
import { QuestSolvePage } from '@/pages/QuestSolvePage'
import { ReflectionPage } from '@/pages/ReflectionPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/campaign" element={<CaseBoardPage />} />
        <Route path="/quest/:questId" element={<QuestStoryPage />} />
        <Route path="/quest/:questId/solve" element={<QuestSolvePage />} />
        <Route path="/quest/:questId/reflection" element={<ReflectionPage />} />
      </Routes>
    </BrowserRouter>
  )
}
