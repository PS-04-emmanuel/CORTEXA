import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ChevronLeft, ChevronRight, FileText, Download } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function History() {
    const [page, setPage] = useState(0)
    const navigate = useNavigate()
    const limit = 6

    const { data: reports, isLoading } = useQuery({
        queryKey: ['reports', page],
        queryFn: async () => {
            const res = await api.get(`/business/reports?skip=${page * limit}&limit=${limit}`)
            return res.data
        }
    })

    return (
        <div className="container mx-auto p-8 max-w-6xl space-y-8">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold tracking-tight">Past Reports</h1>
                <Button variant="outline" onClick={() => navigate('/')}>Back to Analysis</Button>
            </div>

            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3, 4, 5, 6].map(i => (
                        <div key={i} className="h-[250px] bg-muted/20 animate-pulse rounded-lg" />
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {reports?.map((report) => (
                        <Card key={report.id} className="flex flex-col hover:shadow-lg transition-shadow">
                            <CardHeader>
                                <CardTitle className="line-clamp-2 text-lg">{report.prompt}</CardTitle>
                                <div className="text-xs text-muted-foreground">
                                    {new Date(report.created_at).toLocaleDateString()}
                                </div>
                            </CardHeader>
                            <CardContent className="flex-1">
                                <div className="flex justify-between items-center mb-4">
                                    <Badge variant={report.content.feasibility_score > 70 ? "default" : "secondary"}>
                                        Score: {report.content.feasibility_score}
                                    </Badge>
                                </div>
                                <p className="text-sm text-muted-foreground line-clamp-3">
                                    {report.content.summary}
                                </p>
                            </CardContent>
                            <CardFooter>
                                <Button variant="ghost" className="w-full" onClick={async () => {
                                    try {
                                        const response = await api.post(`/business/reports/${report.id}/pdf`, {}, { responseType: 'blob' });
                                        const url = window.URL.createObjectURL(new Blob([response.data]));
                                        const link = document.createElement('a');
                                        link.href = url;
                                        link.setAttribute('download', `report_${report.id}.pdf`);
                                        document.body.appendChild(link);
                                        link.click();
                                        link.parentNode.removeChild(link);
                                    } catch (e) {
                                        alert("Failed to download PDF");
                                    }
                                }}>
                                    <Download className="mr-2 h-4 w-4" /> Download PDF
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            )}

            <div className="flex justify-center gap-4 pt-8">
                <Button
                    variant="outline"
                    onClick={() => setPage(p => Math.max(0, p - 1))}
                    disabled={page === 0}
                >
                    <ChevronLeft className="h-4 w-4 mr-2" /> Previous
                </Button>
                <Button
                    variant="outline"
                    onClick={() => setPage(p => p + 1)}
                    disabled={reports?.length < limit}
                >
                    Next <ChevronRight className="h-4 w-4 ml-2" />
                </Button>
            </div>
        </div>
    )
}
