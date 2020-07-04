# autoJianyu


使用Selenium进行剑鱼网站的自动爬取

# 流程
1. 添加chrome插件，登录
2. 填写搜索关键词
3. 选择中标选项
4. 搜索，获取页面内的所有内容，不断下一页
5. (可能) 点开每个页面获得相关信息
6. 存到csv里面
7. 导出到excel里面


# 使用selenium加载动态网页时

一开始，不管怎么样都加载不出动态页面

然后，开始狗。

`python
driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1]) 
`

就能加载出来了一刚

？？？为啥