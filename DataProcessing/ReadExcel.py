# coding=utf-8
#通过对excel中的测试数据读取执行后将结果写入文件
import json,openpyxl
import xlrd,xlwt
import os
import requests
from Log.logger import log

proDir =  os.path.abspath(os.path.dirname(__file__))
path1=os.path.join(os.path.split(proDir)[0],'GlobalData','test.xlsx')
path2=os.path.join(os.path.split(proDir)[0],'GlobalData','result.xlsx')
def get_requsts(method, url, data, headers, **kwargs):
    if method=="post":
        request_log(url, method, data, headers)
        result = requests.post(url, data, headers).json()  # 封装post方法
        return result

# 将测试结果写excel
def write_data(sheet_name, row, col, value, styleBlueBkg=None):
    copy_excel(path1, path2)
    workbook1 = openpyxl.load_workbook(path2)
    sheet = workbook1[sheet_name]
    sheet.cell(row, col).value = value
    workbook1.save(path2)


def request_log(url, method, data=None,  params=None, headers=None, files=None, cookies=None, **kwargs):
    log.info("接口请求地址 ==>> {}".format(url))
    log.info("接口请求方式 ==>> {}".format(method))
    # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
    log.info("接口请求头 headers参数 ==>> {}".format(headers,ensure_ascii=False))
    log.info("接口请求 params 参数 ==>> {}".format(params,ensure_ascii=False))
    log.info("接口请求体 data 参数 ==>> {}".format(data))
    log.info("接口上传附件 files 参数 ==>> {}".format(files,ensure_ascii=False))
    log.info("接口 cookies 参数 ==>> {}".format(json.dumps(cookies, indent=4, ensure_ascii=False)))

def copy_excel(path1,path2):
    '''复制excel表格，把path1数据复制到path2'''
    wb2=openpyxl.Workbook()
    wb2.save(path2)

    wb1=openpyxl.load_workbook(path1)
    wb2=openpyxl.load_workbook(path2)
    sheets1=wb1.sheetnames
    sheets2=wb2.sheetnames
    sheet1=wb1[sheets1[0]]
    sheet2=wb2[sheets2[0]]
    max_row = sheet1.max_row  # 最大行数
    max_column = sheet1.max_column  # 最大列数

    for m in list(range(1,max_row + 1)):
        for n in list(range(97, 97 + max_column)):  # chr(97)='a'
            n = chr(n)  # ASCII字符
            i = '%s%d' % (n, m)  # 单元格编号
            cell1 = sheet1[i].value  # 获取data单元格数据
            sheet2[i].value = cell1  # 赋值到test单元格
    wb2.save(path2)
    # log.info("{} 复制数据到 {} 成功".format(path1,path2))
    wb1.close()
    wb2.close()




def get_excel(file_path):
    if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        try:
            book = xlrd.open_workbook(file_path)  # 打开excel
            sheet = book.sheet_by_index(0)  # 获取第一个sheet页数据
            for i in range(1, sheet.nrows):  # sheet.nrows获取列表中的每一行
                ex_no = sheet.cell_value(i, 0)  # 用例id
                ex_method = sheet.cell_value(i, 3)  # 请求方法
                ex_header=json.loads(sheet.cell_value(i,4))  #请求头
                ex_url = sheet.cell_value(i, 5)  # 请求url
                ex_data = (sheet.cell_value(i, 6)) # 填写的参数
                ex_res = sheet.cell_value(i, 7)  # 返回json执行结果
                ex_result = sheet.cell_value(i, 8)  # 返回最终通过结果
                ex_pected = sheet.cell_value(i, 9)  # 预期结果
                ex_msg=sheet.cell_value(i,10)  # 返回实际结果的字段
                res = get_requsts(ex_method,ex_url, ex_data,ex_header)  # 调用请求连接方法
                write_data("Sheet", i+1, 8, str(res))
                write_data('Sheet',i+1,11,str(res['errmsg']))
                if res['errmsg'] ==ex_pected:
                    print("{} 测试通过".format(ex_no))  # 判断是否和预期结果一致
                    write_data('Sheet',i+1,9,'Pass',styleBlueBkg=xlwt.easyxf('pattern: pattern solid, fore_colour green'))
                else:
                    write_data('Sheet',i+1,9, 'Fail',styleBlueBkg= xlwt.easyxf('pattern: pattern solid, fore_colour red;'))
                    print('{} 测试失败'.format(ex_no))
        except Exception as e:
            print('this is wrong', e)
    else:
        print('excel格式错误')


if __name__ == '__main__':
    get_excel(path2)
