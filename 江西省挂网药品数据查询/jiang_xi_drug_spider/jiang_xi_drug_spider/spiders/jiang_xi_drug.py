import os
from typing import Any

import scrapy
import csv
import pathlib


class DrugSpider(scrapy.Spider):
    name = 'jiang_xi_drug'
    start_urls = ['https://yp.jxyycg.cn/djypcg/jxyycg/search/medicineRegionBidPriceQry.shtml?dypn=1']
    data_path = pathlib.Path(os.path.abspath("." + os.sep + "jiang_xi_drug.csv"))
    title = ['目录ID',
             '标准通用名',
             '标准剂型',
             '标准规格',
             '包装单位',
             '生产企业',
             '地区',
             '包装数量',
             '最小制剂单位',
             '包装价格',
             '提交时间',
             '备注']

    def parse(self, response: Any) -> Any:
        if not self.data_path.is_file():
            with open(self.data_path.resolve(), "a+", encoding="utf-8", newline='') as file:
                # 第一次创建文件时，写入 title
                csv.writer(file).writerow(self.title)
        with open(self.data_path.resolve(), "a+", encoding="utf-8", newline='') as file:
            # 获取每页所有的词条
            for drug in response.xpath('//tr[@class="hover"]'):
                # 获取单个药品所有信息
                drug_message = drug.xpath('./td/text()').getall()
                csv.writer(file).writerow(drug_message)
        # 判断是否存在下一页
        if "下一页" in response.xpath('//a[@title]/text()').getall():
            base_url, index = response.url.rsplit("=", 1)
            next_page = base_url + "=" + str(int(index) + 1)
            yield scrapy.Request(next_page, callback=self.parse)
