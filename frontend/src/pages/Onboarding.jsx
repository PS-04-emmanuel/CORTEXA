import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

import api from '@/lib/api'

export default function Onboarding() {
    const navigate = useNavigate()

    const [interests, setInterests] = useState([])
    const technologies = ["AI/LLMs", "Blockchain", "Cloud Computing", "IoT", "Cybersecurity", "DevOps"]

    const toggleInterest = (tech) => {
        setInterests(prev =>
            prev.includes(tech) ? prev.filter(t => t !== tech) : [...prev, tech]
        )
    }

    const handleComplete = async () => {
        try {
            await api.put('/users/me/onboard', { interests }) // Sending interests even if backend ignores for now
            navigate('/')
        } catch (error) {
            console.error("Onboarding failed", error)
            alert("Failed to save profile. Please try again.")
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
            <Card className="w-full max-w-lg">
                <CardHeader>
                    <CardTitle className="text-2xl">Welcome to CORTEXA</CardTitle>
                    <p className="text-muted-foreground">Tailor your experience by selecting your interests.</p>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div>
                        <h3 className="text-sm font-medium mb-3">Interested Technologies</h3>
                        <div className="flex flex-wrap gap-2">
                            {technologies.map(tech => (
                                <Badge
                                    key={tech}
                                    variant={interests.includes(tech) ? "default" : "outline"}
                                    className="cursor-pointer text-sm py-1 px-3"
                                    onClick={() => toggleInterest(tech)}
                                >
                                    {tech}
                                </Badge>
                            ))}
                        </div>
                    </div>
                    <Button onClick={handleComplete} className="w-full" size="lg">
                        Complete Profiling & Continue
                    </Button>
                </CardContent>
            </Card>
        </div>
    )
}
