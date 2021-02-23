package routers

import (
	"gitlab.com/bobbae/goex/beego/quickstart/controllers"
	"github.com/astaxie/beego"
)

func init() {
    beego.Router("/", &controllers.MainController{})
}
