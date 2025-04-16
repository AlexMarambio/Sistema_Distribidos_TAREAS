package main

import(
	"fmt" //prints
	"log"
	"github.com/gocolly/colly"
)

func main() {
	collector := colly.NewCollector()
	fmt.Println("Colector creado, iniciando:")
	//buscador
	collector.OnHTML(".wm-rgeocoding",func(e *colly.HTMLElement) {
		fmt.Println(e.Text)
	})
	//gestionar errores
	collector.OnError(func(_ *colly.Response, err error) {
		log.Println("Error:", err)
	})
	//abrir la pagina
	err:=collector.Visit("https://www.waze.com/es-419/live-map/")
	if err != nil {
		log.Fatal(err)
	}
}