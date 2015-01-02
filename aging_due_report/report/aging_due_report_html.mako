<!DOCTYPE>
<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
    <table class="basic_table" width="100%">
        <tr>
            <td width="30%">
                <div  style="float:left;">
                    ${helper.embed_image('jpeg',str(company.logo),180, auto)}
                </div>
            </td>
            <td style="text-align: left;">
                <strong>${_('Customer Aging Report of Debts') |entity}</strong>
            </td>
       </tr>
    </table>
    <% cur_group = get_aged_lines( objects, inv_type='out_invoice') %>
    %for table in cur_group:
        </br>
            <table class="table_column_border table_alter_color_row table_title_bg_color" width="100%">
                <tr>
                    <th width="12%" class="ITEMSTITLELEFT">${_('TIN') |entity}</th>
                    <th width="18%" class="ITEMSTITLELEFT">${_('PARTNER') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">${_('NOT DUE') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">01-30 ${_('DAYS') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">31-60 ${_('DAYS') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">61-90 ${_('DAYS') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">91-120 ${_('DAYS') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">+ 120 ${_('DAYS') |entity}</th>
                    <th width="10%" class="ITEMSTITLERIGHT">${_('TOT./AR')}${"(" + table[0].get('cur_brw', False).name+ ")" |entity}</th>
                </tr>
                %for line in table:
                <tr>
                    <td class="ITEMSLEFT">
                        ${ (line.get('type')=='partner' and line.get('rp_brw').vat and '%s-%s-%s'%(line.get('rp_brw').vat[2],line.get('rp_brw').vat[3:-1],line.get('rp_brw').vat[-1]) or '').upper() }
                    </td>
                    <td class="ITEMSLEFT">
                        <b>${ line.get('type')=='partner' and line.get('rp_brw').name or line.get('type')=='total' and 'TOTAL IN ' + line.get('cur_brw').name or line.get('type')=='provision' and 'PROVISION IN ' + line.get('cur_brw').name }</b>
                    </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('not_due'), digits=2, grouping=True) } </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('1to30'), digits=2, grouping=True) } </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('31to60'), digits=2, grouping=True) } </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('61to90'), digits=2, grouping=True) } </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('91to120'), digits=2, grouping=True) } </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('120+'), digits=2, grouping=True)} </td>
                    <td class="ITEMSRIGHT"> ${formatLang(line.get('total'), digits=2, grouping=True) } </td>
                </tr>
                %endfor
            </table>
    </br>
    %endfor
    <p style="word-wrap:break-word;"></p>

    </br>
    <p style="page-break-before: always;"></p>


</body>
</html>
