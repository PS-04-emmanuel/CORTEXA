import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import api from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function Home() {
    const [prompt, setPrompt] = useState('')
    const navigate = useNavigate()

    const { mutate: generateReport, isPending, data: report } = useMutation({
        mutationFn: async (text) => {
            const res = await api.post('/business/generate-report', { prompt: text })
            return res.data
        }
    })

    const { mutate: generatePdf } = useMutation({
        mutationFn: async (reportId) => {
            const res = await api.post(`/business/reports/${reportId}/pdf`)
            return res.data
        },
        onSuccess: () => {
            alert("PDF Generation started! Check History page.")
        }
    })

    return (
        <div className="container mx-auto p-8 max-w-4xl space-y-8">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold tracking-tight">Business Feasibility AI</h1>
                <div className="flex gap-2">
                    <Button variant="outline" onClick={() => navigate('/history')}>View Past Reports</Button>
                    <Button variant="destructive" onClick={() => {
                        localStorage.removeItem('token')
                        navigate('/login')
                    }}>Log Out</Button>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Analyze a Business Idea</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Textarea
                        placeholder="Describe your business idea (e.g., 'A subscription service for specialized coffee beans sourced from volcanic regions')..."
                        className="min-h-[150px]"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                    <Button
                        onClick={() => generateReport(prompt)}
                        disabled={isPending || !prompt}
                        className="w-full"
                    >
                        {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        {isPending ? 'Analyzing...' : 'Generate Report'}
                    </Button>
                </CardContent>
            </Card>

            {report && (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
                    <Card className="border-primary/20 bg-primary/5">
                        <CardHeader>
                            <div className="flex justify-between">
                                <CardTitle>Analysis Result</CardTitle>
                                <Button variant="default" onClick={() => generatePdf(report.id)}>Download PDF</Button>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-4 bg-background rounded-lg border">
                                    <h3 className="font-semibold mb-2 text-green-600">Pros</h3>
                                    <ul className="list-disc pl-4 space-y-1">
                                        {report.content.pros?.map((p, i) => <li key={i}>{p}</li>)}
                                    </ul>
                                </div>
                                <div className="p-4 bg-background rounded-lg border">
                                    <h3 className="font-semibold mb-2 text-red-600">Cons</h3>
                                    <ul className="list-disc pl-4 space-y-1">
                                        {report.content.cons?.map((c, i) => <li key={i}>{c}</li>)}
                                    </ul>
                                </div>
                            </div>
                            <div>
                                <h3 className="font-semibold mb-2">Detailed Summary</h3>
                                <p className="text-muted-foreground">{report.content.summary}</p>
                            </div>
                            <div>
                                <h3 className="font-semibold mb-2">Economic Analysis</h3>
                                <p className="text-muted-foreground">{report.content.economic_analysis}</p>
                            </div>
                            <div className="text-center pt-4">
                                <span className="text-xl font-bold">Feasibility Score: </span>
                                <span className={`text-2xl font-bold ${report.content.feasibility_score > 70 ? 'text-green-600' : 'text-yellow-600'}`}>
                                    {report.content.feasibility_score}/100
                                </span>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    )
}
