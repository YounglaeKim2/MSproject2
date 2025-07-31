import React from 'react'
import { Routes, Route } from 'react-router-dom'
import styled from 'styled-components'
import HomePage from './pages/HomePage'
import SajuPage from './pages/SajuPage'
import CompatibilityPage from './pages/CompatibilityPage'
import TestPage from './pages/TestPage'
import CyworldSajuTestPage from './pages/CyworldSajuTestPage'

const App = () => {
  return (
    <AppContainer>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/saju" element={<SajuPage />} />
        <Route path="/compatibility" element={<CompatibilityPage />} />
        <Route path="/cyworld-test" element={<CyworldSajuTestPage />} />
      </Routes>
    </AppContainer>
  )
}

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`

export default App